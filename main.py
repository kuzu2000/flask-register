# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from datetime import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'swanthuzaw'
app.config['MYSQL_PASSWORD'] = 'swanthuzaw123@'
app.config['MYSQL_DB'] = 'flask-register'
app.config['SECRET_KEY'] = 'flask-register'
app.config['SESSION_TYPE'] = 'filesystem'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
        phone_number = request.form['phone_number']

        cursor = mysql.connection.cursor()
        hashed_password = sha256_crypt.hash(password)

        cursor.execute("INSERT INTO users (email, username, password, dob, phone_number) VALUES (%s, %s, %s, %s, %s)",
                       (email, username, hashed_password, dob, phone_number))
        mysql.connection.commit()
        cursor.close()

        flash('Registration successful!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        entered_password = request.form['password']

        cursor = mysql.connection.cursor()
        result = cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

        if result > 0:
            user_data = cursor.fetchone()
            hashed_password_db = user_data[3]  # Assuming password is at index 2

            if sha256_crypt.verify(entered_password, hashed_password_db):
                session['logged_in'] = True
                session['username'] = user_data[1]  # Assuming username is at index 1
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password', 'danger')
        else:
            flash('Username not found', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return f"Hello, {session['username']}! This is your dashboard."
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
