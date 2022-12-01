from msilib.schema import tables
from tracemalloc import start
from unicodedata import name
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(120), unique=True)
    mailing_address = db.Column(db.String(120))
    billing_address = db.Column(db.String(120))
    phone_number = db.Column(db.String(120))
    preffered_payment_method = db.Column(db.String(120))
    points = db.Column(db.Integer, default=0)
    password = db.Column(db.String(80))
    account_type = db.Column(db.String(80))
    reservations = db.relationship('Reservation')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    party_size = db.Column(db.Integer)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone_number = db.Column(db.String(120))
    credit_card_number = db.Column(db.String(120))
    credit_card_expiration_date = db.Column(db.String(120))
    credit_card_cvv = db.Column(db.String(120))
    tables  = db.relationship('ReservationTables')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer)
    reservations = db.relationship('ReservationTables')

class ReservationTables(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'))
