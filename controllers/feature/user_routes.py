from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from db import db


user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        existing_user = db.users.find_one({"email": request.form['email']})
        if existing_user:
            flash("Email already registered!")
            return redirect(url_for('user.register'))
        password_hash = generate_password_hash(request.form['password'])
        user_id = db.users.insert_one({
            "email": request.form['email'],
            "password": password_hash,
            "role": "User"
        }).inserted_id
        flash("Registration successful. Please login.")
        return redirect(url_for('user.login'))
    return render_template('register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = db.users.find_one({"email": request.form['email']})
        if user_data and check_password_hash(user_data['password'], request.form['password']):
            user = User(user_data)
            login_user(user)
            return redirect(url_for('user.dashboard'))
        else:
            flash("Invalid username or password")
    return render_template('login.html')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

@user_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('user.html', email=current_user.email)
