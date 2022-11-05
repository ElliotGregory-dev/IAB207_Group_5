from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Event
from .forms import CreateEventForm

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():
    events = Event.query.filter_by().all()
    return render_template('index.html', events=events)


@mainbp.route('/event_details')
def event_details():
    return render_template('event_details.html')


@mainbp.route('/booking_history')
@login_required
def booking_history():
    return render_template('booking_history.html')


@mainbp.route('/create_update')
@login_required
def create_update():
    create_form = CreateEventForm
    return render_template('create_or_update.html', form=create_form)


@mainbp.route('/all_events')
def all_events():
    event = Event.query.all()
    return render_template('all_events.html', data=event)


@mainbp.route('/my_events')
@login_required
def my_events():
    event = Event.query.filter_by(owner_id=current_user.getUserID())
    return render_template('my_events.html', data=event)


@mainbp.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        event = request.args['search']
        events = Event.query.filter(Event.description.like(event)).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))
