from flask import Blueprint, render_template, url_for, redirect, request
from .models import Event, User, Review, Booking
from .forms import CreateEventForm, BuyTicketForm, ReviewForm
from flask_login import login_required, current_user
from datetime import date
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
from time import strftime

# create blueprint
bp = Blueprint('event', __name__, url_prefix='/events')


@bp.route('/<id>',  methods=['GET', 'POST'])
def show(id):
    event = Event.query.filter_by(id=id).first()
    return render_template('event_details.html', event=event, review_form=ReviewForm(), ticket_form=BuyTicketForm())


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
            date_end=create_form.date_end.data,
            status=Event.setStatus(create_form.status.data[0]),
            image=db_file_path,
            time_start=create_form.time_start.data,
            time_end=create_form.time_end.data,
            address=create_form.address.data,
            city=create_form.city.data,
            state=create_form.state.data,
            zip=create_form.zip.data,
            capacity=create_form.capacity.data,
            ticket_price=create_form.ticket_price.data)

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
    
    if review_form_instance.validate_on_submit():  # this is true only in case of POST method
        review = Review(
            event_id=id,
            user_id=current_user.getUserID(),
            date=date.today().strftime("%d/%m/%Y"),
            rating=review_form_instance.rate.data,
            review=review_form_instance.review.data
        )
        db.session.add(review)
        db.session.commit()
        flash(
            f'Review form is valid. The review was {review_form_instance.review.data}')
    else:
        flash('Review form is invalid')
# notice the signature of url_for
    return redirect(url_for('event.show', id=id))


@bp.route("/delete/<id>", methods=['GET', 'POST'])
@login_required
def delete_event(id):
    # this is a function to delete an event
    reviews = Review.query.filter_by(event_id=id)
    for review in reviews:
        review.delete()
    Event.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('main.index'))


@bp.route("/update/<id>/", methods=['GET', 'POST'])
@login_required
def update_event(id):
    event_to_update = Event.query.get_or_404(id)
    update_form = CreateEventForm()

    event_form = CreateEventForm()

    if event_form.validate_on_submit():
        db_file_path = check_upload_file(update_form)
        event_to_update.name = update_form.name.data
        event_to_update.description = update_form.description.data
        event_to_update.date_start = update_form.date_start.data
        event_to_update.date_end = update_form.date_end.data
        event_to_update.image = db_file_path
        event_to_update.status = Event.setStatus(update_form.status.data[0])
        event_to_update.time_start = update_form.time_start.data
        event_to_update.time_end = update_form.time_end.data
        event_to_update.address = update_form.address.data
        event_to_update.city = update_form.city.data
        event_to_update.state = update_form.state.data
        event_to_update.zip = update_form.zip.data
        event_to_update.capacity = update_form.capacity.data
        event_to_update.ticket_price = update_form.ticket_price.data
        # Update to Database
        db.session.add(event_to_update)
        db.session.commit()
        flash("Event Has Been Updated!")
        return redirect(url_for('event.show', id=event_to_update.id))

    update_form.name.data = event_to_update.name
    update_form.description.data = event_to_update.description
    update_form.date_start.data = event_to_update.date_start
    update_form.date_end.data = event_to_update.date_end
    update_form.image = getImageData(event_to_update.image)
    update_form.status = [Event.getStatus(event_to_update)]
    update_form.time_start.data = event_to_update.time_start
    update_form.time_end.data = event_to_update.time_end
    update_form.address.data = event_to_update.address
    update_form.city.data = event_to_update.city
    update_form.state.data = event_to_update.state
    update_form.zip.data = event_to_update.zip
    update_form.capacity.data = event_to_update.capacity
    update_form.ticket_price.data = event_to_update.ticket_price
    return render_template('update.html', form=update_form)


def getImageData(filePath):
    BASE_PATH = os.path.dirname(__file__)
    image_path = os.path.join(
        BASE_PATH, filePath
    )
    return image_path

# add event ticket buying function


@bp.route('/<id>/book/', methods=['GET', 'POST'])
@login_required
def book(id):
    # simple version
    form = BuyTicketForm()

    if form.validate_on_submit():  # this is true only in case of POST method
        event =  Event.query.filter_by(id=id).first()
        bookings = event.getBookings()
        tickets_bought = 0
        for booking in bookings:
            tickets_bought += booking.ticket_amount
        
        if tickets_bought + form.ticket_amount.data > event.capacity:
            flash('too many tickets ordered, try a smaller amount')
            return redirect(url_for('event.show', id=id))

        book = Booking(
            user_id=current_user.getUserID(),
            event_id=id,
            ticket_amount=form.ticket_amount.data,
            date=form.date.data)

        db.session.add(book)
        db.session.commit()
        flash(
            f'Booking form is valid. The Booking was {form.ticket_amount.data}')
    else:
        print('Booking form is invalid')
    # notice the signature of url_for
    return redirect(url_for('event.show', id=id))

    # <<the complete version>>

    # # get how many ticket user buying from the form
    # ticket_buying = form.ticket_amount.data

    # # check capacity from the database
    # tickets_left = Event.query.with_entities(
    #     Event.capacity).filter_by(id=id).first()
    # available_tickets = tickets_left[0]

    # # if the amount of the tickets user buying less than or equal to available tickets
    # if ticket_buying <= available_tickets:

    #     if form.validate_on_submit():
    #         booking = Booking(
    #             # read the bookings from the form
    #             user_id=current_user.getUserID(),
    #             ticket_amount=form.ticket_amount.data,
    #             date=form.date.data)

    #         db.session.add(booking)

    #         # set new capacity to the event
    #         event_to_update = Event.query.get_or_404(id)
    #         event_to_update.capacity = available_tickets - ticket_buying

    #         # set status to sold out if buying ticket equals to capacity
    #         if ticket_buying == available_tickets:
    #             event_to_update.status = 3

    #         db.session.add(event_to_update)

    #         db.session.commit()
    #         message = "The Booking was successful"
    #         flash(message, "success")

    # else:
    #     # if user tries to purchase more tickets than there are available
    #     flash("Not enough tickets available", "warning")
    #     return redirect(url_for("event.show", id=id))

    # return redirect(url_for("event.show", id=id))
