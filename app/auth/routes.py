from flask import render_template, request, redirect, url_for, session, flash, g
from app.auth import bp
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.models.user import User
from icecream import ic
from app.auth.forms import LoginForm, RegisterForm
import functools

@bp.route('/')
def index():
    return render_template('auth/index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if g.user != None:
        message = "You have already registered."
        flash(message=message)
        return redirect(url_for('main.index'))
    form = RegisterForm()
    message = None
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
    if g.user != None:
        message = "You are already logged in."
        flash(message=message)
        return redirect(url_for('main.index'))
    form = LoginForm()
    message = None
    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data
            user = db.session.query(User).where(User.username==username).one()
            if check_password_hash(user.password_hash, password):
                session.clear()
                session['user_id'] = user.id
                message = f"Successfully logged in. Welcome {user.username}"
                flash(message=message)
                return redirect(url_for('main.index'))
            else:
                message = "Incorrect password"
        except Exception as error:
            ic(error)
            message = "An error occurred. Please check your username/password and try again."
        flash(message=message)
    return render_template('auth/login.html', form=form)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            message = "Action not allowed."
            flash(message=message)
            return redirect(url_for('main.index'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/logout')
@login_required
def logout():
    try:
        session.clear()
        message  = "Successfully logged out."
        flash(message=message)
        return redirect(url_for('main.index'))
    except Exception as error:
        ic(error)
        message = "Error in logging out. Or you are not logged in."
        flash(message=message)
        return redirect(url_for('main.index'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        try:
            user = db.session.query(User).where(User.id==user_id).one()
            g.user = user
        except Exception as error:
            ic(error)
            print("[Error in load_logged_in_user]")