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
        gender = request.json.get('gender')
        country = request.json.get('country')
        preferred_language = request.json.get('preferred_language')

        hashed_password = hash_password(password)

        if User.user_exists(username):
            return jsonify({"success": False, "message": "Username already exists"}), 400

        result = User.register(email,username,hashed_password,dob,phone_number, country, preferred_language, gender)

        print(result)

        if result:
            return jsonify({"success": True, "message": "user added"}), 200
        else:
            return jsonify({"success": False, "message": "invalid request format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
