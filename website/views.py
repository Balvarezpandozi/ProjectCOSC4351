from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from .models import Note, Reservation, Table
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
            return redirect(url_for('views.reservations'))

    return render_template('reserve.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)

    if note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted.", category='success')
        return jsonify({'status': 'success'})
    
    return jsonify({'status': 'error'})