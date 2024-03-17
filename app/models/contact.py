from app import db
from sqlalchemy import DateTime
import datetime

# display the date_added as follows
# x.strftime("%y-%B-%d--%H:%M")

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    number = db.Column(db.String(50))
    address = db.Column(db.String(256))
    note = db.Column(db.Text())
    date_added = db.Column(DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return f"<Contact object> - id:{self.id}"