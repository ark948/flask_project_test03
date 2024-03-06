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
    # trying a new approach on message flashing
    # message will be put directly in flash
    new_contact_form = NewContactForm()
    try:
        select_stmt = select(Contact).where(Contact.user_id==current_user.id)
        result = db.session.scalars(select_stmt).all()
        if len(result) == 0:
            flash("Your contact list is empty.")
            contact_list = []
        else:
            contact_list = result
    except Exception as e:
        ic(e)
        flash("An error has occurr")
        return redirect(url_for('contact.index'))
    if new_contact_form.validate_on_submit():
        try:
            contact_object = Contact(new_contact_form.name.data)
            contact_object.number = new_contact_form.number.data
            contact_object.address = new_contact_form.address.data
            contact_object.note = new_contact_form.note.data
            contact_object.user_id = current_user.id
            try:
                db.session.add(contact_object)
                db.session.commit()
            except Exception as contact_insertion_error:
                ic(contact_insertion_error)
                flash('contact insertion error')
                return redirect(url_for('contact.index'))
            flash("Successfully added new contact.")
            return redirect(url_for('contact.index'))
        except Exception as e:
            ic(e)
            flash("An error occurred in adding new contact.")
            return redirect(url_for('contact.index'))
    return render_template('contact/index.html', contact_list=contact_list, new_form=new_contact_form)

@bp.route('/contact/new', methods=['GET', 'POST'])
@login_required
def new():
    return ''