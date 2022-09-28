from msilib.schema import tables
from tracemalloc import start
from unicodedata import name
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(120), unique=True)
    mailingAddress = db.Column(db.String(120))
    billingAddress = db.Column(db.String(120))
    phoneNumber = db.Column(db.String(120))
    prefferedPaymentMethod = db.Column(db.String(120))
    points = db.Column(db.Integer)
    password = db.Column(db.String(80))
    accountType = db.Column(db.String(80))
    reservations = db.relationship('Reservation')
    notes = db.relationship('Note')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.DateTime)
    endTime = db.Column(db.DateTime)
    partySize = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tables  = db.relationship('Table')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'))