from flask import Flask, request, send_from_directory, render_template, Response
import os
from werkzeug.utils import secure_filename
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'Shared Files')
THUMBNAIL_FOLDER = os.path.join(BASE_DIR, 'thumbnails')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['THUMBNAIL_FOLDER'] = THUMBNAIL_FOLDER

def unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    candidate = filename
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], candidate)):
        candidate = f"{base}({counter}){ext}"
        counter += 1
    return candidate

def create_thumbnail(filepath, filename):
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
    video_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', 
                       '.m4v', '.3gp', '.ogv', '.ts', '.m2ts', '.mts', '.vob', 
                       '.asf', '.rm', '.rmvb', '.divx', '.xvid'}
    return os.path.splitext(filename.lower())[1] in video_extensions

def get_files():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.startswith('.') or filename == '.DS_Store':
            continue  # Skip hidden/system files

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        size = os.path.getsize(filepath)
        thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)
        has_thumb = os.path.exists(thumb_path)
        
        # Get file extension for icon
        ext = os.path.splitext(filename.lower())[1][1:]  # Remove the dot
        
        files.append({
            'name': filename,
            'size': format_size(size),
            'thumbnail': f"/thumbnail/{filename}" if has_thumb else None,
            'is_video': is_video_file(filename),
            'extension': ext  # Add extension for consistent icons
        })
    return files

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

@app.route('/')
def index():
    return render_template('index.html', files=get_files())

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        filename = unique_filename(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # create thumbnail if image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            create_thumbnail(filepath, filename)
    return '', 204

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/stream/<path:filename>')
def stream_video(filename):
    def generate():
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'rb') as f:
            data = f.read(1024)
            while data:
                yield data
                data = f.read(1024)
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return "File not found", 404
    
    # Get file size for Content-Length header
    file_size = os.path.getsize(filepath)
    
    # Handle range requests for video seeking
    range_header = request.headers.get('Range', None)
    if range_header:
        byte_start = 0
        byte_end = file_size - 1
        
        if range_header.startswith('bytes='):
            range_match = range_header.replace('bytes=', '').split('-')
            if range_match[0]:
                byte_start = int(range_match[0])
            if range_match[1]:
                byte_end = int(range_match[1])
        
        content_length = byte_end - byte_start + 1
        
        def generate_range():
            with open(filepath, 'rb') as f:
                f.seek(byte_start)
                remaining = content_length
                while remaining:
                    chunk_size = min(8192, remaining)
                    data = f.read(chunk_size)
                    if not data:
                        break
                    remaining -= len(data)
                    yield data
        
        response = Response(
            generate_range(),
            206,  # Partial Content
            headers={
                'Content-Range': f'bytes {byte_start}-{byte_end}/{file_size}',
                'Accept-Ranges': 'bytes',
                'Content-Length': str(content_length),
                'Content-Type': 'video/mp4'  # Default to mp4, browsers are flexible
            }
        )
        return response
    
    # Regular streaming without range
    return Response(
        generate(),
        headers={
            'Content-Length': str(file_size),
            'Content-Type': 'video/mp4',  # Default to mp4, browsers are flexible
            'Accept-Ranges': 'bytes'
        }
    )

@app.route('/thumbnail/<path:filename>')
def serve_thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)