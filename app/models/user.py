from app.db import db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True)
    password_hash = db.Column(db.String(256))

    def __repr__(self) -> str:
        return f'<User {self.id}>'