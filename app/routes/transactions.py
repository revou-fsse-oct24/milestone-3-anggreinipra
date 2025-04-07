from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.transactions import Transaction
from app.models.accounts import Account
from app.database import db
from datetime import datetime
import uuid

transactions_bp = Blueprint('transactions', __name__)

# Util: generate transaction ID
def generate_transaction_id():
    return str(uuid.uuid4())

# POST /transactions-deposit
@transactions_bp.route('/transactions-deposit', methods=['POST'])
@jwt_required()
def deposit():
    data = request.get_json()
    account_number = data.get('account_number')
    amount = float(data.get('amount'))

    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return jsonify({'error': 'Account not found'}), 404

    account.balance += amount
    transaction = Transaction(
        transaction_id=generate_transaction_id(),
        transaction_type='deposit',
        amount=amount,
        balance=account.balance,
        account_id=account.id,
        date_transaction=datetime.utcnow()
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': 'Deposit successful', 'transaction': transaction.to_dict()}), 201


# POST /transactions-withdrawal
@transactions_bp.route('/transactions-withdrawal', methods=['POST'])
@jwt_required()
def withdrawal():
    data = request.get_json()
    account_number = data.get('account_number')
    amount = float(data.get('amount'))

    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return jsonify({'error': 'Account not found'}), 404

    if account.balance < amount:
        return jsonify({'error': 'Insufficient funds'}), 400

    account.balance -= amount
    transaction = Transaction(
        transaction_id=generate_transaction_id(),
        transaction_type='withdrawal',
        amount=amount,
        balance=account.balance,
        account_id=account.id,
        date_transaction=datetime.utcnow()
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': 'Withdrawal successful', 'transaction': transaction.to_dict()}), 201


# POST /transactions-transfer
@transactions_bp.route('/transactions-transfer', methods=['POST'])
@jwt_required()
def transfer():
    data = request.get_json()
    from_account_number = data.get('from_account')
    to_account_number = data.get('to_account')
    amount = float(data.get('amount'))

    from_account = Account.query.filter_by(account_number=from_account_number).first()
    to_account = Account.query.filter_by(account_number=to_account_number).first()

    if not from_account or not to_account:
        return jsonify({'error': 'One or both accounts not found'}), 404

    if from_account.balance < amount:
        return jsonify({'error': 'Insufficient funds'}), 400

    # Transfer logic
    from_account.balance -= amount
    to_account.balance += amount

    # Log both transactions
    t1 = Transaction(
        transaction_id=generate_transaction_id(),
        transaction_type='transfer_out',
        amount=amount,
        balance=from_account.balance,
        account_id=from_account.id,
        date_transaction=datetime.utcnow()
    )
    t2 = Transaction(
        transaction_id=generate_transaction_id(),
        transaction_type='transfer_in',
        amount=amount,
        balance=to_account.balance,
        account_id=to_account.id,
        date_transaction=datetime.utcnow()
    )
    db.session.add_all([t1, t2])
    db.session.commit()

    return jsonify({'message': 'Transfer successful', 'from': t1.to_dict(), 'to': t2.to_dict()}), 201


# GET /transactions → Get all transactions
@transactions_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_all_transactions():
    account_number = request.args.get('account_number')

    if account_number:
        account = Account.query.filter_by(account_number=account_number).first()
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        transactions = Transaction.query.filter_by(account_id=account.id).all()
    else:
        transactions = Transaction.query.all()

    return jsonify([t.to_dict() for t in transactions]), 200


# GET /transactions/<transaction_id> → Get transaction by ID
@transactions_bp.route('/transactions/<string:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction_by_id(transaction_id):
    transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    return jsonify(transaction.to_dict()), 200
