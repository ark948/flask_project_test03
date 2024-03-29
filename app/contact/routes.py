from app.contact import bp
from flask_login import login_required
from flask import render_template, flash, redirect, url_for, request, abort
from app.models.contact import Contact
from sqlalchemy import select, update
from flask_login import current_user
from app import db
from icecream import ic
from app.contact.forms import NewContactForm, UpdateContactForm
import datetime

@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # trying a new approach on message flashing
    # message will be put directly in flash
    new_contact_form = NewContactForm()
    page = request.args.get('page', 1, type=int)
    try:
        pagination = Contact.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=10)
        if pagination.total == 0:
            flash("Your list is empty.")
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
            contact_object.date_added = datetime.datetime.now()
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
    return render_template('contact/index.html', pagination=pagination, new_form=new_contact_form)

@bp.route('/contact/delete/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete(item_id):
    if current_user.is_authenticated:
        try:
            stmt = select(Contact).where(Contact.id==item_id)
            contact_object_to_delete = db.session.scalar(stmt)
            db.session.delete(contact_object_to_delete)
            db.session.commit()
            flash("Item deleted successfully.")
        except Exception as delete_error:
            ic(delete_error)
            flash("Error in deleting item.")
            return redirect(url_for('contact.index'))
    else:
        abort(401)
    return redirect(url_for('contact.index'))

@bp.route('/update/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update(item_id):
    contact_item = Contact.query.filter_by(id=item_id).one()
    form = UpdateContactForm(
        name=contact_item.name,
        number=contact_item.number,
        address=contact_item.address,
        note=contact_item.note
    )

    if form.validate_on_submit():
        contact_item.name=form.name.data
        contact_item.number=form.number.data
        contact_item.address=form.address.data
        contact_item.note=form.note.data
        try:
            db.session.commit()
            flash("update successful")
            return redirect(url_for('contact.index'))
        except Exception as e:
            ic(e)
            flash("error in update")
            return redirect(url_for('contact.index'))
    return render_template('contact/update.html', form=form)