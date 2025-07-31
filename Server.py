from flask import Flask, request, send_from_directory, render_template
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

def get_files():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.startswith('.') or filename == '.DS_Store':
            continue  # Skip hidden/system files

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        size = os.path.getsize(filepath)
        thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)
        has_thumb = os.path.exists(thumb_path)
        files.append({
            'name': filename,
            'size': format_size(size),
            'thumbnail': f"/thumbnail/{filename}" if has_thumb else None
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

@app.route('/thumbnail/<path:filename>')
def serve_thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
