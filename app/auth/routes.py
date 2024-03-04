from flask import render_template, request, redirect, url_for, session, flash, g
from app.auth import bp
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.models.user import User
from icecream import ic
from app.auth.forms import LoginForm
import functools

@bp.route('/')
def index():
    return render_template('auth/index.html')

@bp.route('/register')
def register():
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
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