from flask import render_template, request, redirect, url_for, session, flash, g, current_app
from app.auth import bp
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager, Captcha
from app.models.user import User
from icecream import ic
from app.auth.forms import LoginForm, RegisterForm, ProfileEditForm, PasswordChangeForm, ResetPasswordRequestForm, ResetPasswordForm, VerifyEmailRequestForm
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import select
from app.email import send_email, send_password_reset_email, send_verfiy_email_request_email
from urllib.parse import urlsplit
import datetime


@bp.route('/')
def index():
    return render_template('auth/index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if current_user.is_authenticated:
        flash("You have already registered.")
        return redirect(url_for('main.index'))
    new_captcha_dict = Captcha.create()
    form = RegisterForm()
    if form.validate_on_submit():
        c_hash = request.form['captcha-hash']
        c_text = request.form['captcha-text']
        if Captcha.verify(c_text, c_hash):
            try:
                if form.password.data != form.confirm.data:
                    message = "Passwords do not match. Try again."
                    raise Exception
                new_user = User(username=form.username.data, email=form.email.data)
                new_user.set_password(form.password.data)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    flash("Registration successful.")
                    return redirect(url_for('auth.login'))
                except Exception as new_user_insertioin_error:
                    ic(new_user_insertioin_error)
                    message = "An error occurred during registration, or this username/email is already taken."
            except Exception as registration_error:
                ic(registration_error)
                return redirect(url_for('auth.register'))
        else:
            message="Incorrect captcha."
        flash(message=message)
    return render_template('auth/register.html', form=form, captcha=new_captcha_dict)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if current_user.is_authenticated:
        message = "You are already logged in."
        flash(message=message)
        return redirect(url_for('main.index'))
    new_captcha_dict = Captcha.create()
    form = LoginForm()
    if form.validate_on_submit():
        c_hash = request.form['captcha-hash']
        c_text = request.form['captcha-text']
        if Captcha.verify(c_text, c_hash):
            try:
                username = form.username.data
                password = form.password.data
                user = db.session.query(User).where(User.username==username).one()
                if check_password_hash(user.password_hash, password):
                    login_user(user, remember=form.remember_me.data)
                    current_app.logger.info(f"User with id:{user.id} successfully logged in.")
                    message = "Successfully logged in."
                    flash(message=message)
                    next_page = request.args.get('next')
                    # @login_required decorator helps with this feature
                    if not next_page or urlsplit(next_page).netloc != '':
                        next_page = url_for('main.index')
                    return redirect(next_page)
                else:
                    message = "Incorrect password"
                    current_app.logger.info("Incorrect password.")
            except Exception as error:
                ic(error)
                message = "An error occurred. Please check your username/password and try again."
                current_app.logger.info(f"Failed login attempt.")
        else:
            message="Incorrect Captcha."
        flash(message=message)
    return render_template('auth/login.html', form=form, captcha=new_captcha_dict)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profileForm = ProfileEditForm(
        username=current_user.username,
        email=current_user.email
    )
    passwordForm = PasswordChangeForm()
    return render_template('auth/profile.html', form1=profileForm, form2=passwordForm)

@bp.route('/verify-email-request', methods=['GET', 'POST'])
@login_required
def verify_email_request():
    if current_user.is_confirmed == True:
        flash("Your email has already been verified. If you wish to change your email, you can do it in your profile page. (will require re-verification)")
        return redirect(url_for('main.index'))
    form = VerifyEmailRequestForm()
    if form.validate_on_submit():
        send_verfiy_email_request_email(current_user)
        flash("An email with verification link was sent to your email.")
        return redirect(url_for('main.index'))
    return render_template('auth/verify_email_request.html', form=form)

@bp.route('/verify_email/<token>', methods=['GET', 'POST'])
@login_required
def verify_email(token):
    if current_user.is_confirmed == True:
        flash("Your email has already been verified.")
        return redirect(url_for('main.index'))
    result = User.verify_email_token(token)
    if result:
        try:
            user = User.query.get(current_user.id)
            user.is_confirmed = True
            user.confirmed_on = datetime.datetime.now()
            db.session.commit()
            flash("Successfully verified. Thank you for choosing us.")
            return redirect(url_for('main.index'))
        except Exception as verification_error:
            ic(verification_error)
            flash("Unfortunately, an error occurred during the verification of your email. Please wait 15 minutes and try again. If the issue persists, contact administrator.")
            return redirect(url_for('main.index'))
    return render_template('auth/verify_email.html')

@bp.route('/edit-profile', methods=['POST'])
@login_required
def edit_profile():
    # if user changes their email address, re-verification is required.
    old_email = current_user.email
    ic(">[edit-profile] VIEW INVOKED.")
    user = User.query.get(current_user.id)
    # raise Exception (used to test error logging)
    try:
        if user.username == request.form['username'].strip() and user.email == request.form['email'].strip():
            flash("No changes detected.")
            return redirect(url_for('auth.profile'))
        user.username = request.form['username']
        user.email = request.form['email']
        if user.email != old_email:
            user.is_confirmed = False
            user.confirmed_on = None
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

@bp.route('/reset-password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        flash("You have already logged in. If you can't remember your password, logout first and then use password reset link.")
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        # DO NOT USE TRY AND CATCH TO CHECK IF A USER EXISTS OR NOT AS A SECURITY MEASURE
        user = db.session.scalar(select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('main.index'))
    return render_template('auth/reset_password_request.html', form=form)

@bp.route('/rest_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        flash("You are already logged in. Can't remember? logout first.")
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash("User not found.")
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash("Password reset successful.")
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    message = "Successfully logged out."
    flash(message=message)
    return redirect(url_for('main.index'))