# FileBox
FileBox is a simple, elegant, and lightweight file sharing platform built with Flask. It provides an intuitive interface for uploading, storing, and sharing files with automatic thumbnail generation for images, video streaming capabilities, and real-time upload progress tracking.

---

## Project Overview
FileBox offers a comprehensive file sharing solution designed for:
- **Individual users** looking for a simple file storage solution
- **Teams** needing quick file sharing capabilities  
- **Developers** wanting a lightweight alternative to complex file hosting services
- **Educational purposes** demonstrating modern web development practices

This project focuses on providing a clean, responsive UI/UX with robust backend functionality for file management, featuring drag-and-drop uploads, real-time progress tracking, automatic thumbnail generation, and in-browser video streaming.

---

## Features

### Core Functionality
1. **Multi-File Upload Support**
   - Real-time upload progress with speed and ETA
   
2. **Smart File Management**
   - Automatic duplicate file handling with incremental naming
   - Secure filename sanitization

3. **Image Processing**
   - Automatic thumbnail generation for images
   - Support for multiple image formats (PNG, JPG, JPEG, GIF, BMP, WebP)
   - Optimized thumbnail storage

4. **Video Streaming (NEW!)**
   - In-browser video streaming for all major video formats
   - Support for MP4, AVI, MOV, WMV, FLV, WebM, MKV, and more
   - Range request support for smooth seeking and playback
   - Modal video player with full controls
   - Choose between streaming or downloading videos

5. **Responsive Design**
   - Mobile-first approach
   - Tablet and desktop optimized layouts
   - Modern CSS with smooth animations

### Security & Performance
- Secure file upload handling with Werkzeug
- Input sanitization and validation
- Efficient thumbnail generation with PIL/Pillow
- HTTP range request support for efficient video streaming

---

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AminEfaf/FileBox.git
   cd FileBox
   ```

2. **Install dependencies**
   ```bash
   pip install flask pillow werkzeug
   ```

3. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Run the application**
   ```bash
   python Server.py
   ```

5. **Access the application**
   - Open your browser and navigate to: `http://localhost:8000`

### Production Deployment

For production deployment using Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 Server:app
```
---

## Screenshots

### Desktop Interface
<img width="2880" height="1404" alt="Screenshot 2025-07-31 at 11 10 21" src="https://github.com/user-attachments/assets/93a77c9e-ab5d-410b-88ac-c3b65748aa4b" />
*Clean and modern desktop interface with video streaming support*

### Mobile Interface  
<img src="https://github.com/user-attachments/assets/8497aaa2-2ebf-4960-a3f5-2d201424a8c4" alt="Mobile UI" width="300" />
<p><em>Responsive mobile design optimized for touch interactions</em></p>

### Upload Progress
<img src="https://github.com/user-attachments/assets/8a50015b-59ee-4f13-a944-dc505f427720" alt="Upload progress" width="300" />
<p><em>Real-time upload progress with speed and ETA indicators</em></p>

---

## Technical Details

### Backend (Flask)
- **Framework**: Flask 3.0.0
- **File Handling**: Werkzeug utilities for secure uploads
- **Image Processing**: Pillow for thumbnail generation
- **Video Streaming**: HTTP range request support for efficient streaming
- **Server**: Built-in development server / Gunicorn for production

### Frontend
- **Styling**: Modern CSS3 with Flexbox and Grid
- **JavaScript**: Vanilla ES6+ with class-based architecture
- **Video Player**: HTML5 video with custom modal interface
- **Responsive Design**: Mobile-first CSS media queries
- **Icons**: Unicode emoji icons for universal compatibility

### File Management
- **Upload Directory**: `Shared Files/` (auto-created)
- **Thumbnails**: `thumbnails/` (auto-created)
- **Supported Formats**: All file types with special handling for images and videos
- **Video Formats**: MP4, AVI, MOV, WMV, FLV, WebM, MKV, M4V, 3GP, OGV, TS, M2TS, MTS, VOB, ASF, RM, RMVB, DivX, XviD

---

## Configuration

### Environment Variables
```bash
# Optional: Set custom upload folder
UPLOAD_FOLDER=/path/to/uploads
```

### Customization Options
- Update thumbnail size in `create_thumbnail()` function
- Customize video streaming buffer size in `/stream/<filename>` route
- Add new file type icons in the JavaScript `getFileIcon()` function
- Modify video formats support in `is_video_file()` function

---

## Video Streaming Features

- **Format Support**: Supports all major video formats
- **Efficient Streaming**: Uses HTTP range requests for optimized streaming
- **Responsive Player**: Full-featured video player that works on all devices
- **Dual Action**: Users can choose to either stream videos in-browser or download them
- **Seek Support**: Full seeking capabilities within streamed videos
- **Modal Interface**: Clean, distraction-free video viewing experience

---

## Author

**Mohammad Amin Efaf**
- GitHub: [@aminefaf](https://github.com/aminefaf)
- Email: AminEfaf.82f@gmail.com

---
