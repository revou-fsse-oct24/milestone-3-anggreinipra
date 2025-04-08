from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime

from app.models.transactions import Transaction, TransactionType
from app.models.transfers import Transfer
from app.models.accounts import Account
from app.database import db

transactions_bp = Blueprint('transactions', __name__, url_prefix="/transactions")


# POST /transactions/deposit
@transactions_bp.route('/deposit', methods=['POST'])
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
        transaction_type=TransactionType.DEPOSIT,
        amount=amount,
        balance=account.balance,
        account_number=account.account_number,
        created_at=datetime.utcnow()
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': 'Deposit successful', 'transaction': transaction.to_dict()}), 201


# POST /transactions/withdrawal
@transactions_bp.route('/withdrawal', methods=['POST'])
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
        transaction_type=TransactionType.WITHDRAWAL,
        amount=amount,
        balance=account.balance,
        account_number=account.account_number,
        created_at=datetime.utcnow()
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': 'Withdrawal successful', 'transaction': transaction.to_dict()}), 201


# POST /transactions/transfer
@transactions_bp.route('/transfer', methods=['POST'])
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

    from_account.balance -= amount
    to_account.balance += amount

    transfer = Transfer(
        from_account=from_account.account_number,
        to_account=to_account.account_number,
        amount=amount,
        balance=from_account.balance,  # atau kamu bisa bikin logika sendiri utk balance ini
        created_at=datetime.utcnow()
    )

    db.session.add(transfer)
    db.session.commit()

    return jsonify({'message': 'Transfer successful', 'transfer': transfer.to_dict()}), 201


# GET /transactions
@transactions_bp.route('', methods=['GET'])
@jwt_required()
def get_all_transactions():
    account_number = request.args.get('account_number')

    if account_number:
        account = Account.query.filter_by(account_number=account_number).first()
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        transactions = Transaction.query.filter_by(account_number=account.account_number).all()
    else:
        transactions = Transaction.query.all()

    return jsonify([t.to_dict() for t in transactions]), 200


# GET /transactions/<transaction_id>
@transactions_bp.route('/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction_by_id(transaction_id):
    transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    return jsonify(transaction.to_dict()), 200


# GET /transactions/transfers
@transactions_bp.route('/transfers', methods=['GET'])
@jwt_required()
def get_all_transfers():
    transfers = Transfer.query.all()
    return jsonify([t.to_dict() for t in transfers]), 200


# GET /transactions/transfers/<transfer_id>
@transactions_bp.route('/transfers/<int:transfer_id>', methods=['GET'])
@jwt_required()
def get_transfer_by_id(transfer_id):
    transfer = Transfer.query.filter_by(transfer_id=transfer_id).first()
    if not transfer:
        return jsonify({'error': 'Transfer not found'}), 404
    return jsonify(transfer.to_dict()), 200
