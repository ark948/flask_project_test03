from app import db, login_manager
from flask_login import UserMixin
from app.models.contact import Contact

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(50))
    contacts = db.relationship('Contact', backref='user')


    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash


    def __repr__(self) -> str:
        return f'<User {self.id}>'


@login_manager.user_loader
def load_user(user_id):
    # if user is not found, it will return NoneType which is equal to None
    return User.query.get(user_id)