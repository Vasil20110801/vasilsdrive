import os
from flask import Flask, render_template, request, redirect, send_from_directory

app = Flask(__name__)

# Настройка на папка за качени файлове
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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