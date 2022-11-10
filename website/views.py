from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from .models import Reservation
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def landing():
    return render_template('landing.html', user=current_user)

@views.route('/reservations', methods=['GET'])
@login_required
def reservations():
    reservations = Reservation.query.all()
    return render_template('reservations.html', user=current_user, reservations=reservations)

@views.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        date = list(map(lambda x: int(x), request.form.get('date').split('-')))
        time = list(map(lambda x: int(x), request.form.get('time').split(':')))
        party_size = request.form.get('party-size')
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('phone-number')
        start_date_time = datetime(date[0], date[1], date[2], time[0], time[1])
        end_date_time = datetime(date[0], date[1], date[2], time[0]+1, time[1])
        register_user = request.form.get('register-user')
        print(register_user, flush=True)
        if len(date) < 1:
            flash('Please enter a date.', category='error')
        elif len(time) < 1:
            flash('Please enter a time.', category='error')
        elif len(party_size) < 1:
            flash('Please enter a party size.', category='error')
        elif len(name) < 1:
            flash('Please enter a name.', category='error')
        elif len(email) < 1:
            flash('Please enter an email.', category='error')
        elif len(phone_number) < 1:
            flash('Please enter a phone number.', category='error')
        else:
            if(current_user.is_authenticated):
                user_id = current_user.id
            else:
                user_id = None

            new_reservation = Reservation(
                start_time=start_date_time,
                end_time=end_date_time,
                party_size=party_size,
                name=name,
                email=email,
                phone_number=phone_number,
                user_id=user_id
            )
            db.session.add(new_reservation)
            db.session.commit()
            flash('Reservation created!', category='success')

            if(register_user == "on"):
                return redirect(url_for('auth.register_with_reservation', reservation_id=new_reservation.id))

    return render_template('reserve.html', user=current_user)

@views.route('/edit-reservation/<reservation_id>', methods=['GET', 'POST'])
@login_required
def edit_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)

    if reservation.user_id != current_user.id and current_user.account_type != "admin":
        return redirect(url_for('views.reservations'))

    if request.method == 'POST':
        date = list(map(lambda x: int(x), request.form.get('date').split('-')))
        time = list(map(lambda x: int(x), request.form.get('time').split(':')))
        party_size = request.form.get('party-size')
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('phone-number')
        start_date_time = datetime(date[0], date[1], date[2], time[0], time[1])
        end_date_time = datetime(date[0], date[1], date[2], time[0]+1, time[1])

        if len(date) < 1:
            flash('Please enter a date.', category='error')
        elif len(time) < 1:
            flash('Please enter a time.', category='error')
        elif len(party_size) < 1:
            flash('Please enter a party size.', category='error')
        elif len(name) < 1:
            flash('Please enter a name.', category='error')
        elif len(email) < 1:
            flash('Please enter an email.', category='error')
        elif len(phone_number) < 1:
            flash('Please enter a phone number.', category='error')
        else:
            reservation.start_time = start_date_time
            reservation.end_time = end_date_time
            reservation.party_size = party_size
            reservation.name = name
            reservation.email = email
            reservation.phone_number = phone_number
            db.session.commit()
            flash('Reservation updated!', category='success')
            return redirect(url_for('views.reservations'))
     
    return render_template('edit_reservation.html', user=current_user, reservation=reservation, date=reservation.start_time.strftime('%Y-%m-%d'), time=reservation.start_time.strftime('%H:%M'))
    
@views.route('/delete-reservation', methods=['POST'])
@login_required
def delete_reservation():
    reservation = json.loads(request.data)
    reservation_id = reservation['reservationId']
    reservation = Reservation.query.get(reservation_id)
    if reservation.user_id == current_user.id or current_user.account_type == "admin": 
        db.session.delete(reservation)
        db.session.commit()
    return jsonify({})