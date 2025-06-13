import os
from flask import Flask, render_template, request, redirect, send_from_directory
import os

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

if os.path.exists(UPLOAD_FOLDER):
    if not os.path.isdir(UPLOAD_FOLDER):
        # Ако съществува, но не е папка, изтрий файла и направи папка
        os.remove(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER)
else:
    os.makedirs(UPLOAD_FOLDER)
    # Ако съществува, провери дали е директория
    if not os.path.isdir(UPLOAD_FOLDER):
        raise Exception(f"{UPLOAD_FOLDER} съществува, но не е директория!")
app = Flask(__name__)

import os

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

if os.path.exists(UPLOAD_FOLDER):
    if not os.path.isdir(UPLOAD_FOLDER):
        # Ако съществува, но не е папка, изтрий файла и направи папка
        os.remove(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER)
else:
    os.makedirs(UPLOAD_FOLDER)
# Начална страница – списък с файлове
@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

# Качване на файл
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect('/')
    f = request.files['file']
    if f.filename == '':
        return redirect('/')
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    return redirect('/')

# Изтегляне на файл
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)