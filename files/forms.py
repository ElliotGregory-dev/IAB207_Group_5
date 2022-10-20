from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField,TextAreaField, 
                        Form, IntegerField, FormField, PasswordField, SelectField)
from wtforms.validators import InputRequired, Email, EqualTo

class LoginForm(FlaskForm):
  username = StringField('User Name', validators=[InputRequired()])
  password = PasswordField('Password', validators=[InputRequired()])
  submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('User Name', validators=[InputRequired()])
    email = StringField('Email ID', validators=[InputRequired(),Email() ])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm = PasswordField('Confirm Password', 
          validators=[EqualTo('password', message='Re-enter same as Password')])
    submit = SubmitField('Register')
    
    
