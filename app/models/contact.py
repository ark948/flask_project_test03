from app import db

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    number = db.Column(db.String(50))
    address = db.Column(db.String(256))
    note = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return f"<Contact object> - id:{self.id}"