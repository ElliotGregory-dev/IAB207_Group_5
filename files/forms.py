from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, TimeField, SelectMultipleField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed


ALLOWED_FILE = {'PNG','JPG','png','jpg'}

#Create new event
class EventForm(FlaskForm):
  name = StringField('Event Name:', validators=[InputRequired()])
  description = StringField('Event Description:', 
            validators=[InputRequired()])
  date = DateField('Event Date:', format='%d-%m-%Y', validation=[InputRequired()])
  image = FileField('Attach Image(s):', validators=[
    FileRequired(message='No file selected'),
    FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
  time = TimeField('Event Time:', format='%H:%M - %H:%M', validation=[InputRequired()])
  address= TextAreaField('Address', validators=[InputRequired()])
  city = TextAreaField('City', validators=[InputRequired()])
  state = SelectMultipleField('Choose...', choices=['QLD', 'NSW', 'WA', 'SA', 'TAS', 'NT'],validators=[InputRequired()] )
  zip = IntegerField('Zip',validators=[InputRequired()] )
  capacity = TextAreaField('Event Capacity:',validators=[InputRequired()] )
  ticketprice = IntegerField('Ticket Price:', Length(min=5, max=50))
  submit = SubmitField('Submit')

#User login  
class LoginForm(FlaskForm):
  username = StringField('User Name', validators=[InputRequired()])
  password = PasswordField('Password', validators=[InputRequired()])
  submit = SubmitField('Login')

#User register
class RegisterForm(FlaskForm):
    username = StringField('User Name', validators=[InputRequired()])
    email = StringField('Email ID', validators=[InputRequired(),Email() ])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm = PasswordField('Confirm Password', 
          validators=[EqualTo('password', message='Re-enter same as Password')])
    submit = SubmitField('Register')
    
#User review
class ReviewForm(FlaskForm):
  topic = TextAreaField('Topic', [InputRequired()])
  rate = IntegerField('Rate', Length(min=1, max=5))
  review = TextAreaField('Review', [InputRequired()])
  report_review = SubmitField('ReportReview')
    
    
