from app.contact import bp
from flask_login import login_required
from flask import render_template, flash, redirect, url_for
from app.models.contact import Contact
from sqlalchemy import select
from flask_login import current_user
from app import db
from icecream import ic
from app.contact.forms import NewContactForm

@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    message = None
    new_contact_form = NewContactForm()
    try:
        select_stmt = select(Contact).where(Contact.user_id==current_user.id)
        result = db.session.scalars(select_stmt).all()
        if len(result) == 0:
            message = "Your contact list is empty."
            flash(message=message)
            contact_list = []
        else:
            contact_list = result
    except Exception as e:
        ic(e)
        message = "An error occurred."
        flash(message=message)
        return redirect(url_for('contact.index'))
    return render_template('contact/index.html', contact_list=contact_list, new_contact_form=new_contact_form)

@bp.route('/contact/new', methods=['GET', 'POST'])
@login_required
def new_contact():
    return "Success"