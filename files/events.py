from flask import Blueprint, render_template, url_for, redirect, request
from .models import Event, User
from .forms import CreateEventForm, BuyTicketForm
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

# create blueprint
bp = Blueprint('event', __name__, url_prefix='/events')


@bp.route('/<id>',  methods=['GET', 'POST'])
def show(id):
    event = Event.query.filter_by(id=id).first()
    return render_template('event_details.html', event=event)


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
            image=db_file_path,
            time_start=create_form.time_start.data,
            time_end=create_form.time_end.data,
            address=create_form.address.data,
            city=create_form.city.data,
            state=create_form.state.data,
            zip=create_form.zip.data,
            capacity=create_form.capacity.data,
            ticket_price=create_form.ticketprice.data)

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
