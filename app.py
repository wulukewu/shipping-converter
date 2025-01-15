import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from urllib.parse import unquote

import scripts.Unictron as Unictron
import scripts.DTJ_H as DTJ_H

app = Flask(__name__)

# Configure upload folder and allowed file types
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Checks if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Renders the index page."""
    return render_template('index.html')


@app.route('/Unictron', methods=['GET', 'POST'])
def upload_file_unictron():
    """Handles file upload and processing for Unictron."""
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = unquote(file.filename)
            safe_filename = secure_filename(filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
            file.save(filepath)

            Unictron.organize_data(filepath)

            base_name, extension = os.path.splitext(filename)
            processed_filename = f"{base_name} (processed){extension}"
            processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)

            os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "Organized_Data.xlsx"), processed_filepath)

            return redirect(url_for('download_file', name=processed_filename))

    return render_template('Unictron.html')


@app.route('/DTJ_H', methods=['GET', 'POST'])
def upload_file_dtj_h():
    """Handles file upload and processing for DTJ_H."""
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = unquote(file.filename)
            safe_filename = secure_filename(filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
            file.save(filepath)

            if filename.lower().endswith('.xls'):
                xlsx_filename = os.path.splitext(filepath)[0] + '.xlsx'
                if DTJ_H.convert_xls_to_xlsx(filepath, xlsx_filename):
                    DTJ_H.organize_data_hm(xlsx_filename)
            else:
                DTJ_H.organize_data_hm(filepath)

            base_name, extension = os.path.splitext(filename)
            processed_filename = f"{base_name} (processed).xlsx"
            processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)

            os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "Organized_Data.xlsx"), processed_filepath)

            return redirect(url_for('download_file', name=processed_filename))

    return render_template('DTJ_H.html')


@app.route('/uploads/<name>')
def download_file(name):
    """Sends the processed file to the user for download."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], name, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)