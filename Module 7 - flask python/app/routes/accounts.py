from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import get_all_accounts, get_account_by_id, add_account, update_account, delete_account

bp = Blueprint('accounts', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_accounts():
    user_id = get_jwt_identity()
    return jsonify(get_all_accounts(user_id))

@bp.route('/<int:account_id>', methods=['GET'])
@jwt_required()
def get_account(account_id):
    user_id = get_jwt_identity()
    account = get_account_by_id(account_id)
    if account and account.user_id == user_id:
        return jsonify(account)
    return jsonify({"message": "Unauthorized or account not found"}), 403

@bp.route('/', methods=['POST'])
@jwt_required()
def create_account():
    user_id = get_jwt_identity()
    data = request.get_json()
    account = add_account(user_id, data['account_type'])
    return jsonify(account), 201

@bp.route('/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_account_route(account_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    updated_account = update_account(account_id, user_id, data)
    if updated_account:
        return jsonify(updated_account)
    return jsonify({"message": "Unauthorized or account not found"}), 403

@bp.route('/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_account_route(account_id):
    user_id = get_jwt_identity()
    if delete_account(account_id, user_id):
        return jsonify({"message": "Account deleted"}), 200
    return jsonify({"message": "Unauthorized or account not found"}), 403
