from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Reservation
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('You have been logged in.', category='success')
                return redirect(url_for('views.landing'))
            else:
                flash('Invalid credentials.', category='error')
        else:
            flash('User was not found.', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        mailing_address = request.form.get('mailing-address')
        billing_address_same = request.form.get('billing-mailing-same')
        if billing_address_same == 'on':
            billing_address = mailing_address
        else:
            billing_address = request.form.get('billing-address')
        phone_number = request.form.get('phone-number')
        preffered_payment_method = request.form.get('preffered-payment')

        user = User.query.filter(User.email==email).first()
        print("User " + str(user), flush=True)
        if user:
            flash('User already exists!', category='error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters long.', category='error')
        elif len(name) < 2:
            flash('Name must be at least 2 characters long.', category='error')
        elif password != confirm_password:
            flash('Passwords do not match.', category='error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long.', category='error')
        elif len(mailing_address) < 1:
            flash('Please enter a mailing address.', category='error')
        elif len(billing_address) < 1:
            flash('Please enter a billing address.', category='error')
        elif len(phone_number) < 1:
            flash('Please enter a phone number.', category='error')
        elif len(preffered_payment_method) < 1:
            flash('Please enter a payment method.', category='error')
        else:
            new_user = User(
                name=name, 
                email=email, 
                password=generate_password_hash(password, method='sha256'),
                mailing_address=mailing_address,
                billing_address=billing_address,
                phone_number=phone_number,
                preffered_payment_method=preffered_payment_method,
                points=0,
                account_type="Customer")            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Successfully registered.', category='success')
            return redirect(url_for('views.landing'))

    return render_template('register.html', user=current_user)

@auth.route('/register/<reservation_id>', methods=['GET', 'POST'])
def register_with_reservation(reservation_id):
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        mailing_address = request.form.get('mailing-address')
        billing_address = request.form.get('billing-address')
        phone_number = request.form.get('phone-number')
        preffered_payment_method = request.form.get('preffered-payment')

        user = User.query.filter(User.email==email).first()
        print("User " + str(user), flush=True)
        if user:
            flash('User already exists!', category='error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters long.', category='error')
        elif len(name) < 2:
            flash('Name must be at least 2 characters long.', category='error')
        elif password != confirm_password:
            flash('Passwords do not match.', category='error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long.', category='error')
        elif len(mailing_address) < 1:
            flash('Please enter a mailing address.', category='error')
        elif len(billing_address) < 1:
            flash('Please enter a billing address.', category='error')
        elif len(phone_number) < 1:
            flash('Please enter a phone number.', category='error')
        elif len(preffered_payment_method) < 1:
            flash('Please enter a payment method.', category='error')
        else:
            new_user = User(
                name=name, 
                email=email, 
                password=generate_password_hash(password, method='sha256'),
                mailing_address=mailing_address,
                billing_address=billing_address,
                phone_number=phone_number,
                preffered_payment_method=preffered_payment_method,
                points=0,
                account_type="Customer")            
            db.session.add(new_user)
            reservation = Reservation.query.filter(Reservation.id==reservation_id).first();
            reservation.user_id = new_user.id;
            db.session.commit();
            login_user(new_user, remember=True)
            flash('Successfully registered and reservation added to your account!', category='success')

            return redirect(url_for('views.landing'))
    
    return render_template('register.html', user=current_user, reservation_id=reservation_id)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.landing'))