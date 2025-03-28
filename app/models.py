from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(10), primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    accounts = db.relationship('Account', backref='owner', lazy=True)

class Account(db.Model):
    __tablename__ = 'accounts'
    account_number = db.Column(db.String(20), primary_key=True)
    account_name = db.Column(db.String(50))
    account_type = db.Column(db.String(20))
    balance = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')
    user_id = db.Column(db.String(10), db.ForeignKey('users.user_id'))

class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.String(15), primary_key=True)
    transaction_type = db.Column(db.String(20))
    amount = db.Column(db.Float, nullable=False)
    date_transaction = db.Column(db.DateTime, default=datetime.utcnow)
    account_number = db.Column(db.String(20), db.ForeignKey('accounts.account_number'))
    recipient_account_number = db.Column(db.String(20), nullable=True)
