from multiprocessing.synchronize import Event
from flask import Blueprint, render_template, request, redirect, url_for
from . import ReviewForm
from .models import User
from flask_login import login_required, current_user
from . import db, app
from .models import Event, Review

mainbp = Blueprint('main',__name__)

@mainbp.route('/')
def index():
    u1 = User.query.filter_by(name="user_name").first()
    return render_template('index.html')

@mainbp.route('/event_details')
def event_details():
    return render_template('event_details.html')

@mainbp.route('/booking_history')
def booking_history():
    return render_template('booking_history.html')

@mainbp.route('/create_update')
def create_update():
    return render_template('create_or_update.html')


@mainbp.route('/<id>/review', methods = ['GET', 'POST'])
def review(id):
  #here the form is created  form = ReviewForm()
  form = ReviewForm()
  if form.validate_on_submit():	#this is true only in case of POST method
    print("The following review has been posted:", form.text.data)
  # notice the signature of url_for
  return redirect(url_for('show_event', id=1))


    