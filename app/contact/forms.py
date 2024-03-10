from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class NewContactForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    number = StringField('number')
    address = StringField('address')
    note = TextAreaField('note')
    submit = SubmitField('submit')

class UpdateContactForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    number = StringField('number')
    address = StringField('address')
    note = TextAreaField('note')
    submit = SubmitField('sbumit')