#  FileBox
FileBox is a simple, elegant, and lightweight file sharing platform built with Flask. It provides an intuitive interface for uploading, storing, and sharing files with automatic thumbnail generation for images and real-time upload progress tracking.

---

##  Project Overview
FileBox offers a comprehensive file sharing solution designed for:
- **Individual users** looking for a simple file storage solution
- **Teams** needing quick file sharing capabilities  
- **Developers** wanting a lightweight alternative to complex file hosting services
- **Educational purposes** demonstrating modern web development practices

This project focuses on providing a **clean, responsive UI/UX** with robust backend functionality for file management, featuring drag-and-drop uploads, real-time progress tracking, and automatic thumbnail generation.

---

##  Features

###  Core Functionality
1. **Multi-File Upload Support**
   - Real-time upload progress with speed and ETA
   
2. **Smart File Management**
   - Automatic duplicate file handling with incremental naming
   - Secure filename sanitization
   - File size formatting and validation

3. **Image Processing**
   - Automatic thumbnail generation for images
   - Support for multiple image formats (PNG, JPG, JPEG, GIF, BMP, WebP)
   - Optimized thumbnail storage

4. **Responsive Design**
   - Mobile-first approach
   - Tablet and desktop optimized layouts
   - Modern CSS with smooth animations

###  Security & Performance
- Secure file upload handling with Werkzeug
- File size limitations (100MB default)
- Input sanitization and validation
- Efficient thumbnail generation with PIL/Pillow

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AminEfaf/FileBox.git
   cd FileBox
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Run the application**
   ```bash
   python Server.py
   ```

4. **Access the application**
   - Open your browser and navigate to: `http://localhost:8000`

### Production Deployment

For production deployment using Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

---

## Screenshots

### Desktop Interface
<img width="2880" height="1404" alt="Screenshot 2025-07-31 at 11 10 21" src="https://github.com/user-attachments/assets/93a77c9e-ab5d-410b-88ac-c3b65748aa4b" />
*Clean and modern desktop interface*

### Mobile Interface  
![IMG_3387](https://github.com/user-attachments/assets/8497aaa2-2ebf-4960-a3f5-2d201424a8c4)
*Responsive mobile design optimized for touch interactions*

### Upload Progress
![IMG_3388](https://github.com/user-attachments/assets/8a50015b-59ee-4f13-a944-dc505f427720)
*Real-time upload progress with speed and ETA indicators*

---

## Technical Details

### Backend (Flask)
- **Framework**: Flask 3.0.0
- **File Handling**: Werkzeug utilities for secure uploads
- **Image Processing**: Pillow for thumbnail generation
- **Server**: Built-in development server / Gunicorn for production

### Frontend
- **Styling**: Modern CSS3 with Flexbox and Grid
- **JavaScript**: Vanilla ES6+ with class-based architecture
- **Responsive Design**: Mobile-first CSS media queries
- **Icons**: Unicode emoji icons for universal compatibility

### File Management
- **Upload Directory**: `uploads/` (auto-created)
- **Thumbnails**: `static/thumbnails/` (auto-created)
- **Max File Size**: 100MB (configurable)
- **Supported Formats**: All file types with special handling for images

---

## Configuration

### Environment Variables
```bash
# Optional: Set custom upload folder
UPLOAD_FOLDER=/path/to/uploads

# Optional: Set maximum file size (in bytes)
MAX_CONTENT_LENGTH=104857600  # 100MB
```

### Customization Options
- Modify `MAX_CONTENT_LENGTH` in `app.py` for different file size limits
- Update thumbnail size in `create_thumbnail()` function
- Customize styling in `static/css/main.css`
- Add new file type icons in `main.js`

---

## Author

**Mohammad Amin Efaf**
- GitHub: [@aminefaf](https://github.com/aminefaf)
- Email: AminEfaf.82f@gmail.com
