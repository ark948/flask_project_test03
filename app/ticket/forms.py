from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app.models.ticket import Ticket_Category
from app import db
from sqlalchemy import select

class NewTicketForm(FlaskForm):
    category = SelectField('category', validate_choice=[DataRequired()])
    subject = StringField('subject', validators=[DataRequired()])
    body = TextAreaField('body', validators=[DataRequired()])
    # skip attachment for now
    submit = SubmitField('submit')