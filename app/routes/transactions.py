from flask import Blueprint, request, jsonify
from app.models import Transaction, Account, db

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.route("/", methods=["POST"])
def create_transaction():
    data = request.get_json()
    transaction = Transaction(
        transaction_id=data['transaction_id'],
        transaction_type=data['transaction_type'],
        amount=data['amount'],
        account_number=data['account_number'],
        recipient_account_number=data.get('recipient_account_number')
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction created"}), 201
