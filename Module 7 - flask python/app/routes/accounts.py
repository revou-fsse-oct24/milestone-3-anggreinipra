from flask import Blueprint, request, jsonify
from app.models import get_all_accounts, get_account_by_id, add_account, update_account, delete_account

bp = Blueprint('accounts', __name__)

@bp.route('/', methods=['GET'])
def get_accounts():
    return jsonify(get_all_accounts())

@bp.route('/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account = get_account_by_id(account_id)
    if account:
        return jsonify(account)
    return jsonify({"message": "Account not found"}), 404

@bp.route('/', methods=['POST'])
def create_account():
    data = request.get_json()
    account = add_account(data['account_type'])
    return jsonify(account), 201

@bp.route('/<int:account_id>', methods=['PUT'])
def update_account_route(account_id):
    data = request.get_json()
    updated_account = update_account(account_id, data)
    if updated_account:
        return jsonify(updated_account)
    return jsonify({"message": "Account not found"}), 404

@bp.route('/<int:account_id>', methods=['DELETE'])
def delete_account_route(account_id):
    if delete_account(account_id):
        return jsonify({"message": "Account deleted"}), 200
    return jsonify({"message": "Account not found"}), 404