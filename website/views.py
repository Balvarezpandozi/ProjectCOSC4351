from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from .models import Reservation, Table, ReservationTables
from .highTrafficMonitoring import check_for_high_traffic
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
        date = request.form.get('date')
        time = request.form.get('time')
        party_size = request.form.get('party-size')
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('phone-number')
        register_user = request.form.get('register-user')
        credit_card_number = request.form.get('credit-card-number')
        credit_card_expiration_date = request.form.get('credit-card-expiration-date')
        credit_card_cvv = request.form.get('credit-card-cvv') 
        
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

            date = list(map(lambda x: int(x), date.split('-')))
            time = list(map(lambda x: int(x), time.split(':')))

            start_date_time = datetime(date[0], date[1], date[2], time[0], time[1])
            end_date_time = datetime(date[0], date[1], date[2], time[0], time[1])

            if not check_time_range(start_date_time):
                flash('Please enter a time between 10:00 AM and 9:00 PM.', category='error')
                return render_template('reserve.html', user=current_user)

            dateDict = {
                'year': date[0],
                'month': date[1],
                'day': date[2]
            }

            if check_for_high_traffic(dateDict) and (credit_card_number == "" or credit_card_expiration_date == "" or credit_card_cvv == ""):
                flash('Please enter credit card info.', category='error')
                return render_template('reserve.html', user=current_user)

            new_reservation = Reservation(
                start_time=start_date_time,
                end_time=end_date_time,
                party_size=party_size,
                name=name,
                email=email,
                phone_number=phone_number,
                user_id=user_id,
                credit_card_number= credit_card_number,
                credit_card_expiration_date= credit_card_expiration_date,
                credit_card_cvv= credit_card_cvv
            )
            db.session.add(new_reservation)
            db.session.flush()

            # Get tables
            table_1 = Table.query.filter_by(id=1).first()
            table_2 = Table.query.filter_by(id=2).first()

            # Create relationships
            table1Relationship = ReservationTables(
                reservation_id = new_reservation.id,
                table_id = table_1.id
            )

            table2Relationship = ReservationTables(
                reservation_id = new_reservation.id,
                table_id = table_2.id
            )

            db.session.add(table1Relationship)
            db.session.add(table2Relationship)
            db.session.commit()
            flash('Reservation created!', category='success')

            if(register_user == "on"):
                return redirect(url_for('auth.register_with_reservation', reservation_id=new_reservation.id))

    return render_template('reserve.html', user=current_user)

@views.route('/edit-reservation/<reservation_id>', methods=['GET', 'POST'])
@login_required
def edit_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    reservation_tables = ReservationTables.query.filter_by(reservation_id = reservation_id).all() 

    if reservation.user_id != current_user.id and current_user.account_type != "admin":
        return redirect(url_for('views.reservations'))

    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        party_size = request.form.get('party-size')
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('phone-number')
        credit_card_number = request.form.get('credit-card-number')
        credit_card_expiration_date = request.form.get('credit-card-expiration-date')
        credit_card_cvv = request.form.get('credit-card-cvv')

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
            date = list(map(lambda x: int(x), date.split('-')))
            time = list(map(lambda x: int(x), time.split(':')))
            start_date_time = datetime(date[0], date[1], date[2], time[0], time[1])
            end_date_time = datetime(date[0], date[1], date[2], time[0], time[1])

            if not check_time_range(start_date_time):
                flash('Please enter a time between 10:00 AM and 9:00 PM.', category='error')
                return render_template('edit_reservation.html', user=current_user, reservation=reservation, date=reservation.start_time.strftime('%Y-%m-%d'), time=reservation.start_time.strftime('%H:%M'))

            if check_for_high_traffic(start_date_time) and (credit_card_number == "" or credit_card_expiration_date == "" or credit_card_cvv == ""):
                flash('Please enter credit card info.', category='error')
                return render_template('edit_reservation.html', user=current_user, reservation=reservation, date=reservation.start_time.strftime('%Y-%m-%d'), time=reservation.start_time.strftime('%H:%M'))


            reservation.start_time = start_date_time
            reservation.end_time = end_date_time
            reservation.party_size = party_size
            reservation.name = name
            reservation.email = email
            reservation.phone_number = phone_number

            map(db.session.delete, reservation_tables)
            # Get tables
            table_1 = Table.query.filter_by(id=1).first()
            table_2 = Table.query.filter_by(id=2).first()

            # Create relationships
            table1Relationship = ReservationTables(
                reservation_id = reservation.id,
                table_id = table_1.id
            )

            table2Relationship = ReservationTables(
                reservation_id = reservation.id,
                table_id = table_2.id
            )

            db.session.add(table1Relationship)
            db.session.add(table2Relationship)

            reservation.credit_card_number = credit_card_number
            reservation.credit_card_expiration_date = credit_card_expiration_date
            reservation.credit_card_cvv = credit_card_cvv
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

@views.route('/high-traffic', methods=['POST']) 
def high_traffic():
    if request.method == 'POST':
        data = json.loads(request.data)
        date = data['date'].split('-')
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        dateDict = {
            'year': year,
            'month': month,
            'day': day
        }
        isHighTraffic = check_for_high_traffic(dateDict)
        return jsonify({"isHighTraffic": isHighTraffic})

def check_time_range(start_time):
    hour = start_time.hour
    # Openning hours between 10am and 10pm
    if hour < 10 or hour > 21:
        return False
    return True
    