from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '354ewR24VD2VSD4F5uijmcdjDF2G4D5'
socketio = SocketIO(app)
users = {}


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if username in users:
            error = 'یوزر نیم از قبل وجود دارد.'
        elif not password == confirm_password:
            error = 'پسورد دوم مطابق با پسورد اول نیست'
        else:
            users[username] = {
                'username': username,
                'password': generate_password_hash(password)
            }
            return redirect(url_for('login'))
        return render_template('register.html', error=error)
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        error = 'پسورد یا نام کاربری اشتباه است!'
        return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@socketio.on('message')
def handle_message(message):
    emit('message', {'username': session['username'], 'message': message}, broadcast=True)


if __name__ == '__main__':
    app.secret_key = '354ewR24VD2VSD4F5uijmcdjDF2G4D5'
    socketio.run(app, debug=True)
