from flask import Blueprint, request, jsonify
from app.models import Account, db

accounts_bp = Blueprint("accounts", __name__)

@accounts_bp.route("/", methods=["GET"])
def get_accounts():
    accounts = Account.query.all()
    return jsonify([{
        "account_number": account.account_number,
        "account_name": account.account_name,
        "account_type": account.account_type,
        "balance": account.balance,
        "status": account.status,
        "user_id": account.user_id
    } for account in accounts]), 200

@accounts_bp.route("/", methods=["POST"])
def create_account():
    data = request.get_json()
    account = Account(
        account_number=data['account_number'],
        account_name=data['account_name'],
        account_type=data['account_type'],
        balance=data['balance'],
        user_id=data['user_id']
    )
    db.session.add(account)
    db.session.commit()
    return jsonify({"message": "Account created"}), 201
