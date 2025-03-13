from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import get_transactions, get_transaction_by_id, add_transaction

bp = Blueprint('transactions', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_all_transactions():
    user_id = get_jwt_identity()
    return jsonify(get_transactions(user_id))

@bp.route('/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    user_id = get_jwt_identity()
    transaction = get_transaction_by_id(transaction_id)
    if transaction and transaction.account_owner == user_id:
        return jsonify(transaction)
    return jsonify({"message": "Unauthorized or transaction not found"}), 403

@bp.route('/', methods=['POST'])
@jwt_required()
def create_transaction():
    user_id = get_jwt_identity()
    data = request.get_json()
    transaction = add_transaction(user_id, data['account_id'], data['amount'], data['transaction_type'])
    return jsonify(transaction), 201
