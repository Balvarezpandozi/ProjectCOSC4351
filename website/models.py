from msilib.schema import tables
from tracemalloc import start
from unicodedata import name
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Use camelCase for models because of issues with sqlAlchemy. In everything else, use snake_case.

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(120), unique=True)
    mailing_address = db.Column(db.String(120))
    billing_address = db.Column(db.String(120))
    phone_number = db.Column(db.String(120))
    preffered_payment_method = db.Column(db.String(120))
    points = db.Column(db.Integer)
    password = db.Column(db.String(80))
    account_type = db.Column(db.String(80))
    reservations = db.relationship('Reservation')
    notes = db.relationship('Note')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    party_size = db.Column(db.Integer)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone_number = db.Column(db.String(120))
    tables  = db.relationship('Table')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'))