from flask import Blueprint,render_template

mainbp = Blueprint('main',__name__)

@mainbp.route('/')
def index():
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