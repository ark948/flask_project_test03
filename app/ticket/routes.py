from app.ticket import bp
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.ticket.forms import NewTicketForm
from app.models.ticket import Ticket, Ticket_Status, Ticket_Category
from app import db, Captcha
from sqlalchemy import select
from icecream import ic
import datetime, secrets

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user_tickets = Ticket.query.filter_by(sender=current_user.id).all()
    return render_template('ticket/index.html', tickets=user_tickets)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = NewTicketForm()
    category_items = db.session.scalars(select(Ticket_Category)).all()  
    form.category.choices = [(1, 'Registration Problem'), (2, 'Login Problem'), (3, 'Site functinonality'), (4, 'Bug report'), (5, 'Other...')]
    new_captcha_dict = Captcha.create()
    if form.validate_on_submit():
        c_hash = request.form['captcha-hash']
        c_text = request.form['captcha-text']
        if Captcha.verify(c_text, c_hash):
            new_ticket = Ticket()
            new_ticket.sender = current_user.id
            new_ticket.receiver = 9 # current only admin id
            new_ticket.status_id = 3
            new_ticket.category_id = int(form.category.data)
            new_ticket.subject = form.subject.data
            new_ticket.body = form.body.data
            new_ticket.attachment = None # for now
            new_ticket.date_created = datetime.datetime.now()
            new_ticket.previous_ticket = None # for now
            new_ticket.next_ticket = None
            new_ticket.confirm_code = secrets.randbelow(100_000_000) # first must perform a exist in db check
            new_ticket.no_reply = None # for now
            new_ticket.read_only = None # for now
            try:
                db.session.add(new_ticket)
                db.session.commit()
                flash(f'Ticket submitted successfully. Please wait apprx. 24 hours for a reply from one of the admins. {new_ticket.confirm_code}')
                return redirect(url_for('ticket.index'))
            except Exception as error:
                ic(error)
                flash("An error occurred. We are sorry.")
                return redirect(url_for('ticket.index'))
    return render_template('ticket/new.html', form=form, captcha=new_captcha_dict)

@bp.route('/view/<int:confirm_code>')
@login_required
def view(confirm_code):
    ticket = db.session.scalar(select(Ticket).where(Ticket.sender==current_user.id).where(Ticket.confirm_code==confirm_code))
    return render_template('ticket/view.html', ticket=ticket)