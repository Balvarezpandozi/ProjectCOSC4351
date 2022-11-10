from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from . import db
from .models import User, Reservation, Table
import json

administrator = Blueprint('administrator', __name__)

@administrator.route('/')
@login_required
def load_admin_portal():
    if current_user.account_type == 'admin':
        reservations = Reservation.query.all()
        tables = Table.query.all()
        users = User.query.all()

        return render_template('admin.html', user=current_user, reservations=reservations, tables=tables, users=users)
    else:
        return redirect(url_for('views.landing'))

@administrator.route('/add-table', methods=['POST'])
@login_required
def add_table():
    if current_user.account_type == 'admin':
        table = Table(capacity=request.form.get('capacity'))
        db.session.add(table)
        db.session.commit()
        return redirect(url_for('administrator.load_admin_portal'))
    else:
        return redirect(url_for('administrator.load_admin_portal'))

@administrator.route('/delete-table', methods=['POST'])
@login_required
def delete_table():
    table = json.loads(request.data)
    table_id = table['tableId']
    table = Table.query.get(table_id)
    if current_user.account_type == 'admin': 
        db.session.delete(table)
        db.session.commit()
    return jsonify({})

@administrator.route('/delete-user', methods=['POST'])
@login_required
def delete_user():
    user = json.loads(request.data)
    user_id = user['userId']
    user = User.query.get(user_id)
    if current_user.account_type == 'admin': 
        db.session.delete(user)
        db.session.commit()
    return jsonify({})

@administrator.route('/set-admin')
@login_required
def set_admin():
    print("add administrator account", flush=True)
    if User.query.filter_by(account_type='admin').first() is None:
        print("Inside if statement", flush=True)
        admin_user = User(
                name="admin", 
                email="admin@admin.com", 
                password=generate_password_hash("admin", method='sha256'),
                mailing_address= None,
                billing_address= None,
                phone_number= None,
                preffered_payment_method= None,
                points=0,
                account_type="admin")            
        db.session.add(admin_user)
        db.session.commit()
        print("after commiting database", flush=True)
    return redirect(url_for('views.landing'))