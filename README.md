🎓 Smart AI Attendance System (v3.0)
AI-Powered Biometric Attendance with Cloud Integration
🚀 Overview
This project is an advanced Computer Vision application designed to automate student attendance at Technocrats Institute of Technology (TIT), Bhopal. By leveraging Deep Learning, the system eliminates manual paperwork, identifying students via face recognition and syncing data in real-time to a Cloud Database (Google Sheets).

🛠️ Tech Stack
Language: Python 3.x

AI Engine: DeepFace (Facenet CNN Architecture)

Frontend UI: Streamlit (Neon-Glassmorphism UI)

Cloud Integration: GSheets API (Persistent Storage)

Biometrics: Streamlit-WebRTC (Live browser-based camera streaming)

Data Analytics: Pandas, Matplotlib, and Plotly

🌟 Key Features
Two-Factor Authentication: Combines User Credentials (ID/Pass) with Biometric Face Verification.

Live Cloud Syncing: Attendance records are automatically appended to a Google Sheet for global accessibility.

Time-Session Management: Includes logic for Morning (9:15 AM - 10:30 AM) and Evening sessions.

Anti-Duplicate Logic: Prevents multiple attendance entries for the same student within a single session.

Interactive Dashboard: Real-time visualization of attendance percentage and branch-wise distribution.

One-Time Enrollment: Simple registration process that saves face baseline data permanently.

🧠 Core Concepts Applied
Mathematics: Coordinate Geometry (Facial Landmarks), Euclidean Distance (Face Matching), and Time-Series Data Management.

Data Science: Data Cleaning/Wrangling, Real-time API Integration, and Statistical Analytics.

📂 Repository Structure
Plaintext
├── app.py                # Main Application Logic
├── requirements.txt      # Python Dependencies
├── packages.txt          # System-level Dependencies (libgl1)
└── dataset/              # Student Face Data (Organized by Username)
     └── ritesh/          # Example: Baseline images for user 'ritesh'
👨‍💻 Developer
Ritesh Kumar Singh B.Tech CSE (Data Science) Technocrats Institute of Technology (TIT), Bhopal ---
