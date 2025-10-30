# app/user_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.Models import db, User , Chat
from flask_login import login_required, current_user , logout_user , login_user


user_bp = Blueprint('user_bp', __name__)


















# --------------- home Route ---------------

@user_bp.route('/')
def home():
    return render_template('home.html')




# --------------- register Route ---------------

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login.')
            return redirect(url_for('user_bp.login'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please login.')
        return redirect(url_for('user_bp.login'))

    return render_template('register.html')






# --------------- login Route ---------------


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)  # ✅ logs in user and sets session automatically
            flash('Login successful!')
            return redirect(url_for('chat.dashboard'))
        else:
            flash('Invalid email or password.')

    return render_template('login.html')



# -------------------- logout Route ------------------

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()  
    flash('You have been logged out.')
    return redirect(url_for('user_bp.login'))



