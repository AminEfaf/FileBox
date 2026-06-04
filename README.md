<div align="center">

# 📦 FileBox

**A lightweight, self-hosted file sharing platform built with Flask.**  
Upload, store, and share files instantly — with video streaming, image thumbnails, and QR code access.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey?logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
</div>

---

## What is FileBox?

FileBox is a minimal, self-hosted file sharing server you run on your local network. No cloud, no accounts, no limits. Open the browser on any device on the same network, upload files, and access them instantly — including streaming videos directly in the browser.

**Designed for:** home networks, small teams, developers, and anyone who wants a simple alternative to cloud storage for local sharing.

---

## Features

- **Multi-file upload** with real-time progress, speed, and ETA
- **Video streaming** — watch MP4, MKV, AVI, MOV, WebM and more directly in the browser
- **Image thumbnails** — auto-generated previews for PNG, JPG, GIF, WebP, BMP
- **QR code access** — click the title to get a QR code; scan from any phone to open instantly
- **Smart duplicate handling** — auto-renames files instead of overwriting
- **Secure filenames** — sanitized with Werkzeug before saving
- **Responsive design** — works on desktop, tablet, and mobile
- **Zero config** — runs out of the box with a single command

---

## Quick Start

### Option 1 — One-click launch (recommended)

```bash
# macOS / Linux
chmod +x Start.sh && ./Start.sh

# Windows — double-click Start.bat
```

The script will automatically create a virtual environment, install dependencies, and open your browser.

### Option 2 — Manual setup

**1. Clone the repository**
```bash
git clone https://github.com/AminEfaf/FileBox.git
cd FileBox
```

**2. Create a virtual environment**
```bash
python3 -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run**
```bash
python3 Server.py
```

**5. Open** `http://localhost:8000` in your browser.

---

## Accessing from other devices

FileBox binds to `0.0.0.0`, so any device on the same network can access it.

1. Find your machine's local IP — it's shown in the terminal on startup, or click the **FileBox** title in the app for a QR code
2. On any phone or device connected to the same Wi-Fi, open `http://<your-ip>:8000`
3. Or just scan the QR code

---

## Project structure

```
FileBox/
├── Server.py              # Flask backend
├── requirements.txt       # Python dependencies
├── Start.sh               # One-click launcher (macOS/Linux)
├── Start.bat              # One-click launcher (Windows)
├── templates/
│   └── index.html         # Main UI template
├── static/
│   ├── style.css          # All styles
│   └── main.js            # All JavaScript
├── Shared Files/          # Uploaded files (auto-created)
└── thumbnails/            # Generated thumbnails (auto-created)
```

---

## Technical details

| Layer | Stack |
|-------|-------|
| Backend | Python 3.8+, Flask 2.3+, Werkzeug |
| Image processing | Pillow |
| QR code | pyqrcode + pypng |
| Frontend | Vanilla HTML5, CSS3, ES6+ JavaScript |
| Video streaming | HTTP range requests (RFC 7233) |
| Server | Flask dev server / Gunicorn |

---

## AI Assistance Disclosure

This project was developed with the assistance of [Claude](https://claude.ai) (Anthropic) for code generation, debugging, refactoring, and documentation. All code has been reviewed, tested, and is maintained by the author. The use of AI assistance is disclosed in the interest of transparency.

---

## License

[MIT](LICENSE) — free to use, modify, and distribute.

---

## Author

**Mohammad Amin Efaf**  
GitHub: [@AminEfaf](https://github.com/AminEfaf)  
Email: Amin.Efaf@outlook.com

---

<div align="center">
  <sub>If FileBox is useful to you, consider giving it a ⭐ — it helps others find it.</sub>
</div>
