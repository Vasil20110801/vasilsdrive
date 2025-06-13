from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Настройки
app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB

db = SQLAlchemy(app)


# Модели
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# Създаване на директория, ако я няма
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Начална страница
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(session['user_id']))
    os.makedirs(user_folder, exist_ok=True)

    files = os.listdir(user_folder)
    files = sorted([f for f in files if os.path.isfile(os.path.join(user_folder, f))])

    return render_template('drive.html', files=files)


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(username=username).first():
            flash('Този потребител вече съществува!')
            return redirect(url_for('register'))

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Успешна регистрация!')
        return redirect(url_for('login'))

    return render_template('register.html')


# Логин
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        flash('Невалидни данни за вход.')
        return redirect(url_for('login'))

    return render_template('login.html')


# Изход
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# Качване на файл
@app.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(session['user_id']))
        os.makedirs(user_folder, exist_ok=True)
        file.save(os.path.join(user_folder, filename))
    return redirect(url_for('index'))


# Сваляне на файл
@app.route('/download/<filename>')
def download(filename):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(session['user_id']))
    return send_from_directory(user_folder, filename, as_attachment=True)


# Изтриване на файл
@app.route('/delete/<filename>')
def delete(filename):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(session['user_id']))
    path = os.path.join(user_folder, filename)
    if os.path.exists(path):
        os.remove(path)
    return redirect(url_for('index'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
app.run(debug=True)