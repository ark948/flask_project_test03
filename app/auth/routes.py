from flask import render_template, request, redirect, url_for, session, flash, g
from app.auth import bp
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from app.models.user import User
from icecream import ic
from app.auth.forms import LoginForm, RegisterForm, ProfileEditForm, PasswordChangeForm 
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
                message = "Successfully logged in."
                flash(message=message)
                return redirect(url_for('main.index'))
            else:
                message = "Incorrect password"
        except Exception as error:
            ic(error)
            message = "An error occurred. Please check your username/password and try again."
        flash(message=message)
    return render_template('auth/login.html', form=form)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profileForm = ProfileEditForm(
        username=current_user.username,
        email=current_user.email
    )
    passwordForm = PasswordChangeForm()
    return render_template('auth/profile.html', form1=profileForm, form2=passwordForm)

@bp.route('/edit-profile', methods=['POST'])
@login_required
def edit_profile():
    ic(">[edit-profile] VIEW INVOKED.")
    user = User.query.get(current_user.id)
    try:
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        flash("Profile info updated successfully.")
    except Exception as db_integrity_error:
        ic(db_integrity_error)
        flash('An error occurred. Most likely the username/email you entered is already taken.')
    return redirect(url_for('auth.profile'))

@bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    ic(">[change-password] VIEW INVOKED.")
    user = User.query.get(current_user.id)
    try:
        if request.form['password'] == request.form['confirm']:
            if check_password_hash(user.password_hash, request.form['password']):
                try:
                    user.password_hash = generate_password_hash(request.form['new_password'])
                    db.session.commit()
                    flash("Password changed successfully.")
                except Exception as e:
                    ic(e)
                    flash("Sorry, error occurred.")
            else:
                ic("Bad Hash")
                flash("Incorrect password.")
        else:
            ic("ERROR")
            flash("Passwords do not match.")
    except Exception as e:
        ic("line 120")
        flash("Unknown error.")
    return redirect(url_for('auth.profile'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    message = "Successfully logged out."
    flash(message=message)
    return redirect(url_for('main.index'))