from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, TimeField, SelectMultipleField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import validators


ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg'}

# Create new event


class CreateEventForm(FlaskForm):
    name = StringField('Event Name:', validators=[InputRequired()])
    description = StringField('Event Description:',
                              validators=[InputRequired()])

    # date_start = DateField('Event Date Start:',
    #                        format='%d-%m-%Y', validators=[InputRequired()])
    # date_end = DateField('Event Date End:', format='%d-%m-%Y',
    #                      validators=[InputRequired()])
    date_start = StringField('Event Date Start:', validators=[InputRequired()])
    date_end = StringField('Event Date End:', validators=[InputRequired()])
    status = SelectMultipleField('Event Status:', validators=[InputRequired()], choices=[
                                 'open', 'cancelled', 'sold-out', 'unpublished'])
    image = FileField('Attach Image(s):', validators=[
        FileRequired(message='No file selected'),
        FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
    # time_start = TimeField('Event Time Start:', format='%H:%M - %H:%M', validators=[InputRequired()])
    # time_end = TimeField('Event Time End:', format='%H:%M - %H:%M', validators=[InputRequired()])
    time_start = StringField('Event Time Start:', validators=[InputRequired()])
    time_end = StringField('Event Time End:', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    # state = SelectMultipleField('Choose...', choices=['QLD', 'NSW', 'WA', 'SA', 'TAS', 'NT'],validators=[InputRequired()] )
    state = StringField('State', validators=[InputRequired()])
    zip = StringField('Zip', validators=[InputRequired()])
    capacity = IntegerField('Event Capacity:', validators=[InputRequired()])
    ticket_price = IntegerField('Ticket Price:', [validators.NumberRange(
        min=5, max=50, message="The price should be at least $5 and maximum $50")])
    submit = SubmitField('Submit')

# Ticket


class BuyTicketForm(FlaskForm):
    ticket_amount = IntegerField('How many: ', validators=[Length(min=1)])
    date = StringField('Date:', validators=[InputRequired()])
    submit = SubmitField("Buy")


# User login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")

# User register


class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[
                           Email("Please enter a valid email"), InputRequired()])
    ph_num = StringField("Phone Number", validators=[InputRequired()])

    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")

# User review


class ReviewForm(FlaskForm):
    # topic = TextAreaField('Topic', [InputRequired()])
    date = StringField('Date', [InputRequired()])
    rate = IntegerField('Rate', [validators.NumberRange(
        min=1, max=5, message="The rating should be from 1 to 5")])
    review = TextAreaField('Review', [InputRequired()])
    submit = SubmitField('Write Review')
