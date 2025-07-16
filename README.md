# 📡 SnapShare

SnapShare is a lightweight local network tool built with Flask that allows users on the same WiFi network to:

- 📤 Upload and share text or files
- 📥 Download shared files on other devices
- 🧭 (Optional) View connected devices via `nmap` scan (local use only)

---

## 🚀 Features

- 🔁 Real-time shared text input and display
- 📁 File upload and download across devices
- ⏳ Auto-deletion of uploaded files after 5 minutes or after download
- 💻 Network device detection using `nmap` (only works locally)
- ⚙️ Modern UI with responsive design and animations

---

## 🧠 How It Works

- Text and file input is shared via Flask backend
- All devices connected to the same WiFi network can view/download the content
- Uploaded files are deleted automatically after being downloaded (or after 5 mins)
- Optional: Uses `nmap` to detect devices (only supported in local environments)

---

## 📂 Project Structure
          SnapShare/
          ├── app.py # Main Flask app
          ├── file_feature.py # File upload/download logic
          ├── requirements.txt # Python dependencies
          ├── templates/
          │ └── index.html # Jinja2 HTML template
          ├── uploads/ # Temporary upload storage (auto-cleared)
          ├── README.md # Project info

---

## ⚙️ Setup & Run Locally

```bash
git clone https://github.com/yourusername/snapshare.git
cd snapshare

# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open your browser at:
<a href="http://localhost:5000" target="_blank" rel="noopener noreferrer">http://localhost:5000</a>

---

## 📦 Requirements

```
Python 3.7+
Flask
python-nmap (optional, for scanning)
nmap installed on your system (for local use)
```
---
## 🙋‍♂️ Author
<b>Abdul Manan</b>
