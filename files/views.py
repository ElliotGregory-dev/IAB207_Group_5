from flask import Blueprint,render_template, request, redirect, url_for
from .models import User, Event

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

@mainbp.route('/all_events')
def all_events():
    return render_template('all_events.html')
@mainbp.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        event = "%" + request.args['search'] + '%'
        events = Event.query.filter(Event.description.like(event)).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))
