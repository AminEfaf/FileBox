#!/usr/bin/env python3

from flask import Flask, request, send_from_directory, render_template, Response
import os
import io
import socket
from werkzeug.utils import secure_filename
from PIL import Image
import pyqrcode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'Shared Files')
THUMBNAIL_FOLDER = os.path.join(BASE_DIR, 'thumbnails')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['THUMBNAIL_FOLDER'] = THUMBNAIL_FOLDER


# ── Helpers ────────────────────────────────────────────────────────────────────

def unique_filename(filename):
    """Return a non-colliding filename by appending a counter when needed."""
    base, ext = os.path.splitext(filename)
    counter = 1
    candidate = filename
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], candidate)):
        candidate = f"{base}({counter}){ext}"
        counter += 1
    return candidate


def create_thumbnail(filepath, filename):
    """Generate a 120×120 thumbnail for image files."""
    thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)
    try:
        with Image.open(filepath) as img:
            img.thumbnail((120, 120))
            img.save(thumb_path)
        return True
    except Exception as e:
        print(f"Thumbnail creation failed for {filename}: {e}")
        return False


def is_video_file(filename):
    video_extensions = {
        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv',
        '.m4v', '.3gp', '.ogv', '.ts', '.m2ts', '.mts', '.vob',
        '.asf', '.rm', '.rmvb', '.divx', '.xvid'
    }
    return os.path.splitext(filename.lower())[1] in video_extensions


def get_files():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.startswith('.') or filename == '.DS_Store':
            continue

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        size = os.path.getsize(filepath)
        thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)
        has_thumb = os.path.exists(thumb_path)
        ext = os.path.splitext(filename.lower())[1][1:]

        files.append({
            'name': filename,
            'size': format_size(size),
            'thumbnail': f"/thumbnail/{filename}" if has_thumb else None,
            'is_video': is_video_file(filename),
            'extension': ext,
            'mtime': os.path.getmtime(filepath),
        })

    files.sort(key=lambda f: f['mtime'], reverse=True)
    return files


def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html', files=get_files())


@app.route('/qr')
def qr_code_route():
    """Return a QR-code PNG pointing at this server's local URL."""
    ip = get_local_ip()
    port = 8000
    url = f"http://{ip}:{port}"

    qr = pyqrcode.create(url)
    buffer = io.BytesIO()
    qr.png(buffer, scale=6)
    buffer.seek(0)

    return Response(buffer.getvalue(), mimetype='image/png')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        filename = unique_filename(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            create_thumbnail(filepath, filename)

    return '', 204


@app.route('/download/<path:filename>')
def download_file(filename):
    if '..' in filename or filename.startswith('/'):
        return "Invalid filename", 400
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return "File not found", 404
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/stream/<path:filename>')
def stream_video(filename):
    if '..' in filename or filename.startswith('/'):
        return "Invalid filename", 400
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return "File not found", 404

    file_size = os.path.getsize(filepath)
    range_header = request.headers.get('Range')

    if range_header:
        byte_start = 0
        byte_end = file_size - 1

        if range_header.startswith('bytes='):
            parts = range_header.replace('bytes=', '').split('-')
            if parts[0]:
                byte_start = int(parts[0])
            if parts[1]:
                byte_end = int(parts[1])

        content_length = byte_end - byte_start + 1

        def generate_range():
            with open(filepath, 'rb') as f:
                f.seek(byte_start)
                remaining = content_length
                while remaining:
                    chunk = min(8192, remaining)
                    data = f.read(chunk)
                    if not data:
                        break
                    remaining -= len(data)
                    yield data

        return Response(
            generate_range(),
            status=206,
            headers={
                'Content-Range': f'bytes {byte_start}-{byte_end}/{file_size}',
                'Accept-Ranges': 'bytes',
                'Content-Length': str(content_length),
                'Content-Type': 'application/octet-stream',
            }
        )

    def generate_full():
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(8192)
                if not data:
                    break
                yield data

    return Response(
        generate_full(),
        headers={
            'Content-Length': str(file_size),
            'Content-Type': 'application/octet-stream',
            'Accept-Ranges': 'bytes',
        }
    )


@app.route('/thumbnail/<path:filename>')
def serve_thumbnail(filename):
    if '..' in filename or filename.startswith('/'):
        return "Invalid filename", 400
    thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)
    if not os.path.exists(thumb_path):
        return "Thumbnail not found", 404
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
