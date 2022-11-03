from flask import Blueprint, render_template, url_for, redirect, request
from .models import Event, User, Review
from .forms import CreateEventForm, BuyTicketForm, ReviewForm
from flask_login import login_required, current_user
from datetime import datetime
from . import db
import os
from flask_wtf.form import FlaskForm
from sqlalchemy.databases import mysql, sqlite
from sqlalchemy import func
from sqlalchemy.sql.functions import user
from werkzeug.exceptions import abort
import sqlalchemy
from sqlalchemy.engine import create_engine
from werkzeug.utils import secure_filename
from flask.helpers import flash
from time import strftime, strptime

# create blueprint
bp = Blueprint('event', __name__, url_prefix='/events')


@bp.route('/<id>',  methods=['GET', 'POST'])
def show(id):
    event = Event.query.filter_by(id=id).first()
    return render_template('event_details.html', event=event, review_form=ReviewForm())


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_update():
    create_form = CreateEventForm()
    print('Method type: ', request.method)
    if create_form.validate_on_submit():
        db_file_path = check_upload_file(create_form)
        event = Event(
            owner_id=current_user.getUserID(),
            name=create_form.name.data,
            description=create_form.description.data,
            date_start=create_form.date_start.data,
            date_end=str(create_form.date_end.data),
            image=db_file_path,
            time_start=str(create_form.time_start.data),
            time_end=str(create_form.time_end.data),
            address=create_form.address.data,
            city=create_form.city.data,
            state=create_form.state.data,
            zip=create_form.zip.data,
            capacity=str(create_form.capacity.data),
            ticket_price=str(create_form.ticketprice.data))

        db.session.add(event)
        db.session.commit()
        message = "The list has been created successfully"
        flash(message, "success")
        print('Successfully created a new Event', 'success')
        return redirect(url_for('event.create_update'))

    return render_template('create_or_update.html', form=create_form)


def check_upload_file(form):
    # get file data from form
    fp = form.image.data
    filename = fp.filename
    # get the current path of the module file… store image file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_path = os.path.join(
        BASE_PATH, 'static/img', secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/img/' + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path


@bp.route('/<id>/review', methods=['GET', 'POST'])
@login_required
def review(id):
    review_form_instance = ReviewForm()
    review = Review(
        event_id=id,
        user_id=current_user.getUserID(),
        date=review_form_instance.date.data,
        rating=review_form_instance.rate.data,
        review=review_form_instance.review.data
    )
    db.session.add(review)
    db.session.commit()
    if review_form_instance.validate_on_submit():  # this is true only in case of POST method
        print(
            f'Review form is valid. The review was {review_form_instance.review.data}')
    else:
        print('Review form is invalid')
# notice the signature of url_for
    return redirect(url_for('event.show', id=id))


@bp.route("/delete/<id>", methods=['GET', 'POST'])
@login_required
def delete_event(id):
    # this is a function to delete an event
    event_to_delete = Event.query.get_or_404(id)

    try:
        db.session.delete(event_to_delete)
        db.session.commit()
        return redirect(url_for('main.index'))
    except:
        return "There was a problem deleting the event"


@bp.route("/listed/<id>/updated", methods=['GET', 'POST'])
@login_required
def edit_component(id):

    user = Event.query.filter_by(id=id)
    auction_item = CreateEventForm()
# currently empty function

    return render_template('auctions/update.html', id=id, user=user, form=auction_item)
