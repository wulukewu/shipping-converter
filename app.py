import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
import main  # Import your existing script
from urllib.parse import unquote # Import unquote

app = Flask(__name__)

# Configure upload folder and allowed file types
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Checks if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Handles file upload and processing."""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = unquote(file.filename) # Unquote the filename
            safe_filename = secure_filename(filename) # Use secure_filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
            file.save(filepath)

            # Process the file using your main.py script
            main.organize_data(filepath)

            # --- Modify output filename here ---
            base_name, extension = os.path.splitext(filename)
            processed_filename = f"{base_name} (processed){extension}"
            processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)

            # Rename the output file from main.py
            os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "Organized_Data.xlsx"), processed_filepath)

            return redirect(url_for('download_file', name=processed_filename))

    return render_template('index.html')


@app.route('/uploads/<name>')
def download_file(name):
    """Sends the processed file to the user for download."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], name, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)