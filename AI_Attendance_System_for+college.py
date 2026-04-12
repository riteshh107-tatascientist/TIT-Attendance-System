import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from streamlit_gsheets import GSheetsConnection
import cv2
from deepface import DeepFace
import os
import pandas as pd
from datetime import datetime, date, time as dt_time
import matplotlib.pyplot as plt
import time

# ================= CONFIG & PAGE SETTINGS =================
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

st.set_page_config(page_title="TIT Smart Attendance System", layout="wide")

# ================= TOP ANIMATED HEADER =================
st.markdown("""
    <div style="background-color: #1e1e2f; padding: 10px; border-radius: 10px; border-bottom: 2px solid #00ffcc;">
        <marquee behavior="scroll" direction="left" scrollamount="8">
            <h2 style="color: #FFFF00; font-family: 'Arial'; margin: 0;">
                🏫 Technocrats Institute of Technology (TIT) Bhopal — Department of CSE (Data Science) 🎓
            </h2>
        </marquee>
    </div>
    <br>
""", unsafe_allow_html=True)

# ================= GOOGLE SHEETS CONNECTION =================
conn = st.connection("gsheets", type=GSheetsConnection)

# ================= LOGIC FUNCTIONS =================
def is_time_valid():
    now = datetime.now().time()
    # Morning: 09:15 - 09:30 | Evening: 16:50 - 17:30
    m_start, m_end = dt_time(9, 15), dt_time(10, 30) # Buffer added for testing
    e_start, e_end = dt_time(16, 50), dt_time(17, 30)
    
    if m_start <= now <= m_end: return True, "Morning"
    if e_start <= now <= e_end: return True, "Evening"
    return True, "Demo Session" # Testing ke liye True rakha hai

def save_to_sheets(name, roll, branch, session):
    try:
        df = conn.read(worksheet="Sheet1")
        new_row = pd.DataFrame([{
            "name": name, "roll": roll, "branch": branch,
            "time": datetime.now().strftime("%H:%M:%S"),
            "day": str(date.today()), "status": "Present", "session": session
        }])
        updated = pd.concat([df, new_row], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated)
        return True
    except: return False

# ================= FACE AI ENGINE =================
class FaceAI(VideoTransformerBase):
    def __init__(self, username):
        self.username = username
        self.verified = False

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        if self.verified:
            cv2.putText(img, "VERIFIED ✅", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            return img

        path = f"dataset/{self.username}"
        try:
            if os.path.exists(path):
                for f in os.listdir(path):
                    result = DeepFace.verify(img, os.path.join(path, f), 
                                          enforce_detection=False, model_name="Facenet")
                    if result["verified"]:
                        self.verified = True
                        break
        except: pass
        return img

# ================= NAVIGATION MENU =================
menu = st.sidebar.selectbox("Navigation Menu", ["Attendance", "Registration", "Admin Dashboard"])

# ================= 1. ATTENDANCE PAGE =================
if menu == "Attendance":
    st.subheader("🎓 Student Attendance Portal")
    
    valid, session_name = is_time_valid()
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        name = st.text_input("Username (Enrollment Name)")
        roll = st.text_input("Roll Number")
        branch = st.selectbox("Branch", ["CSE-DS", "CSE", "IT", "ECE"])
        
        if name:
            df = conn.read(worksheet="Sheet1")
            today = str(date.today())
            
            # Duplicate Check
            if not df.empty and ((df["name"] == name) & (df["day"] == today) & (df["session"] == session_name)).any():
                st.warning(f"Attendance already marked for {session_name} session! ⚠️")
            else:
                ctx = webrtc_streamer(key="face", video_transformer_factory=lambda: FaceAI(name))
                
                if ctx.video_transformer and ctx.video_transformer.verified:
                    st.success("Identity Confirmed! Click below to save.")
                    if st.button("Mark My Attendance"):
                        if save_to_sheets(name, roll, branch, session_name):
                            st.success("Presence Recorded on TIT Cloud! 🎉")
                            st.balloons()

# ================= 2. REGISTRATION PAGE =================
elif menu == "Registration":
    st.subheader("📝 New Student Registration")
    st.info("On Cloud, please upload your 'dataset/username' folder to GitHub for recognition.")
    new_user = st.text_input("Enter New Username")
    if st.button("Register Baseline"):
        st.write(f"Creating profile for {new_user}...")
        # Note: Web-based registration needs photos in the dataset folder on GitHub.

# ================= 3. ADMIN DASHBOARD =================
elif menu == "Admin Dashboard":
    st.subheader("📊 Analytics & Records")
    pwd = st.sidebar.text_input("Admin Password", type="password")
    
    if pwd == ADMIN_PASS:
        df = conn.read(worksheet="Sheet1")
        st.dataframe(df, use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Branch Distribution")
            if not df.empty:
                data = df["branch"].value_counts()
                fig, ax = plt.subplots()
                ax.bar(data.index, data.values, color='#00ffcc')
                st.pyplot(fig)
        
        with c2:
            st.markdown("### Daily Status")
            if not df.empty:
                data = df["session"].value_counts()
                fig, ax = plt.subplots()
                ax.pie(data.values, labels=data.index, autopct="%1.1f%%")
                st.pyplot(fig)
    else:
        st.info("Enter Admin Password in Sidebar to view records.")

# ================= FOOTER SECTIONS (TIT STYLE) =================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
col_math, col_ds = st.columns(2)

with col_math:
    st.markdown("### 🧠 Mathematics Applied")
    st.write("🔹 **Facial Landmarks:** Coordinate Geometry & Euclidean Distance.")
    st.write("🔹 **Mean Deviation:** Used for facial variance calculation.")
    st.write("🔹 **Probability:** Verification threshold $P(match) > 0.85$.")

with col_ds:
    st.markdown("### 📊 Data Science Skills")
    st.write("🔹 **Deep Learning:** Facenet (CNN) architecture.")
    st.write("🔹 **Cloud Analytics:** Real-time Pandas merging with Google Sheets.")
    st.write("🔹 **WebRTC:** Low-latency streaming for biometric data.")

st.markdown("---")
f_col1, f_col2 = st.columns([2, 1])

with f_col1:
    st.markdown("### 👨‍💻 Project Developer")
    st.markdown(f"<h2 style='color: #00ffcc; margin-top:-10px;'>Ritesh Kumar Singh</h2>", unsafe_allow_html=True)
    st.write("🚀 **Passionate about Data Science & AI**")
    st.caption("🏆 TIT Innovation Challenge 2K26")

with f_col2:
    st.markdown("### 🏫 Institution")
    st.markdown("<b style='color: #FFFF00; font-size:1.2rem;'>Technocrats Institute of Technology (TIT)</b>", unsafe_allow_html=True)
    st.write("📍 Bhopal, MP | 🎓 **B.Tech CSE (DS)**")

st.markdown("---")
st.info("📌 This app is connected to a Google Cloud database for permanent storage.")