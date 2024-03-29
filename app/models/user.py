from app import db, login_manager
from flask_login import UserMixin
from app.models.contact import Contact
from time import time
import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(50))
    is_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    contacts = db.relationship('Contact', backref='user')


    def __init__(self, username, email):
        self.username = username
        self.email = email
        # self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<User {self.id}>'
    
    def get_verify_email_token(self, expires_in=600):
        return jwt.encode(
            {'verify_email': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_email_token(token):
        try:
            result = jwt.decode(token, current_app.config['SECRET_KEY'],
                                algorithms=['HS256'])['verify_email']
        except Exception as error:
            return error
        return True
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            # returns None
            return
        return db.session.get(User, id)


@login_manager.user_loader
def load_user(user_id):
    # if user is not found, it will return NoneType which is equal to None
    return User.query.get(user_id)