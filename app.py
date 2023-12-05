# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from passlib.hash import sha256_crypt
from datetime import datetime
from model.User import User

app = Flask(__name__)

def hash_password(password):
    return sha256_crypt.using(rounds=1000).hash(password)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        dob = datetime.strptime(request.json.get('dob'), '%Y-%m-%d')
        phone_number = request.json.get('phone_number')

        hashed_password = hash_password(password)

        result = User.register(email,username,hashed_password,dob,phone_number)

        print(result)

        if result:
            return jsonify({"success": True, "message": "user added"}), 200
        else:
            return jsonify({"success": False, "message": "invalid request format"}), 400

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
