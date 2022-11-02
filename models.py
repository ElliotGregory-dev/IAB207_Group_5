from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)#should be 128 in length to store hash

    def __repr__(self):
        return "<Name: {}, id: {}>".format(self.name, self.id)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    date = db.Column(db.String(100))
    image = db.Column(db.String(400))
    time = db.Column(db.String(5))
    address = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip = db.Column(db.String(6))
    capacity = db.Column(db.String(10))
    ticketprice = db.Column(db.String(10))
    
	
    def __repr__(self): #string print method
        return "<Name: {}>".format(self.name)