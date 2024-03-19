from app import db
import datetime
from sqlalchemy import DateTime

# ticket table fields: id, sender, receiver, status, category, title(subject), body, attachment, date_created, previous,
# next-ticket, confirm-code, no-reply, read-only

# precautions about attachment fields: storing images and such in database is not recommended, instead one should
# store them in static folder, and store their retrieval in database

# category table fields: ...

# status table fields: pending-review, accepted, declined, awaiting-user-reply, resolved

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # rel -> user.id/admin.id
    receiver = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False) # rel -> user.id/admin.id
    status_id = db.Column(db.Integer, db.ForeignKey('ticket_status.id'), nullable=False) # rel -> status table id
    category_id = db.Column(db.Integer, db.ForeignKey('ticket_category.id'), nullable=False) # rel -> cateogry table id
    subject = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    attachment = db.Column(db.String(512), nullable=True) # just string (address of file, pointing to uploads folder)
    date_created = db.Column(DateTime, default=datetime.datetime.now)
    previous_ticket = db.Column(db.Integer, db.ForeignKey('ticket.id')) # rel -> ticket.id
    next_ticket = db.Column(db.Integer, db.ForeignKey('ticket.id')) # rel -> ticket.id
    confirm_code = db.Column(db.Integer, nullable=False, unique=True) # generate in code using secrets module
    no_reply = db.Column(db.Boolean, nullable=True)
    read_only = db.Column(db.Boolean, nullable=True)

class Ticket_Status(db.Model):
    __tablename__ = 'ticket_status'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

class Ticket_Category(db.Model):
    __tablename__ = 'ticket_category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Ticket_Category {self.title}>'