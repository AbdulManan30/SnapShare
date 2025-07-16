import os

UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def handle_file_upload(request):
    """Save uploaded file and return filename (or empty string)."""
    uploaded_file = request.files.get("file")
    if uploaded_file and uploaded_file.filename != "":
        filename = uploaded_file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        uploaded_file.save(file_path)
        return filename
    return ""

def get_latest_uploaded_file():
    """Return the most recent uploaded filename, or empty string."""
    files = sorted(
        [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))],
        key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x))
    )
    return files[-1] if files else ""

def delete_all_files():
    """Delete all files in upload folder."""
    for f in os.listdir(UPLOAD_FOLDER):
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, f))
        except:
            pass
