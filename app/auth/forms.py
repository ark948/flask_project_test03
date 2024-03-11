from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('confirm')])
    confirm = PasswordField('confirm', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProfileEditForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PasswordChangeForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired(), EqualTo('confirm')])
    confirm = PasswordField('confirm', validators=[DataRequired()])
    new_password = PasswordField('new', validators=[DataRequired()])
    submit = SubmitField('Submit')