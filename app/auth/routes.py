from flask import render_template, request, redirect, url_for, session, flash, g
from app.auth import bp
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from app.models.user import User
from icecream import ic
from app.auth.forms import LoginForm, RegisterForm
import functools
from flask_login import current_user, login_user, login_required, logout_user


@bp.route('/')
def index():
    return render_template('auth/index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if current_user.is_authenticated:
        message = "You have already registered."
        flash(message=message)
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            email = form.username.data
            password = form.password.data
            confirm = form.confirm.data
            if password != confirm:
                message = "Passwords do not match. Try again."
                raise Exception
            new_user = User(username=username, email=email, password_hash=generate_password_hash(password))
            try:
                db.session.add(new_user)
                db.session.commit()
                message = "Registration successful."
                flash(message=message)
                return redirect(url_for('auth.login'))
            except Exception as new_user_insertioin_error:
                ic(new_user_insertioin_error)
                message = "An error occurred during registration, or this username/email is already taken."
        except Exception as registration_error:
            ic(registration_error)
            return redirect(url_for('auth.register'))
        flash(message=message)
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if current_user.is_authenticated:
        message = "You are already logged in."
        flash(message=message)
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data
            user = db.session.query(User).where(User.username==username).one()
            if check_password_hash(user.password_hash, password):
                login_user(user, remember=form.remember_me.data)
                message = "User successfully logged in."
                flash(message=message)
                return redirect(url_for('main.index'))
            else:
                message = "Incorrect password"
        except Exception as error:
            ic(error)
            message = "An error occurred. Please check your username/password and try again."
        flash(message=message)
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    message = "Successfully logged out."
    flash(message=message)
    return redirect(url_for('main.index'))