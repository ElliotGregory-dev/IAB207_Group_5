from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    ph_number = db.Column(db.Integer, nullable=False)
    # should be 128 in length to store hash
    password_hash = db.Column(db.String(255), nullable=False)

    def getUserID(self):
        return self.id

    def __repr__(self):
        return "<Name: {}, id: {}>".format(self.name, self.id)

# add availability to Event data


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100))
    status = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    date_start = db.Column(db.String(20))
    date_end = db.Column(db.String(20))
    image = db.Column(db.String(400))
    time_start = db.Column(db.String(10))
    time_end = db.Column(db.String(10))
    address = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip = db.Column(db.String(6))
    capacity = db.Column(db.Integer)
    ticket_price = db.Column(db.Integer)

    reviews = db.relationship('Review', backref='event')

    def getOwnerDetails(self):
        return User.query.filter_by(id=self.user_id)

    def getStatus(self):
        if(self.status == 1):
            return "open"
        elif(self.status == 2):
            return "unpublished"
        elif(self.status == 3):
            return "sold-out"
        elif(self.status == 4):
            return "cancelled"

    def setStatus(status):
        if(status == "open"):
            return 1
        elif(status == "unpublished"):
            return 2
        elif(status == "sold-out"):
            return 3
        elif(status == "cancelled"):
            return 4

    def getReviews(self):
        return Review.query.filter_by(event_id=self.id)

    def getBookings(self):
        return Booking.query.filter_by(event_id=self.id)

    def __repr__(self):  # string print method
        return "<Name: {}>".format(self.name)


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Integer)
    review = db.Column(db.String(500))

    user = db.relationship('User')



    def getEventDetails(self):
        return Event.query.filter_by(id=self.event_id)

    def getUserDetails(self):
        return User.query.filter_by(id=self.user_id)

    def __repr__(self):
        return "<Name: {}, id: {}, event: {}, user: {}>".format(self.name, self.id, self.event_id, self.user_id)


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    ticket_amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(20), nullable=False)

    def getUserDetails(self):
        return User.query.filter_by(id=self.user_id)

    def __repr__(self):
        return "<Name: {}, id: {}, user_id: {}>".format(self.name, self.id, self.user_id)
