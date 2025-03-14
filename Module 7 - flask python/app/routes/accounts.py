from flask import Blueprint, request, jsonify
from app.models import (
    get_all_accounts, get_account_by_id, add_account,
    update_account, delete_account
)

bp = Blueprint('accounts', __name__, url_prefix='/accounts')

@bp.route('/', methods=['GET'])
def get_accounts():
    """Mengembalikan semua akun"""
    accounts = get_all_accounts()
    return jsonify(accounts), 200

@bp.route('/<string:account_id>', methods=['GET'])
def get_account(account_id):
    """Mengembalikan detail akun berdasarkan ID"""
    account = get_account_by_id(account_id)
    if account:
        return jsonify(account), 200
    return jsonify({"message": "Account not found"}), 404

@bp.route('/', methods=['POST'])
def create_account():
    """Membuat akun baru"""
    data = request.get_json()
    if not data or "account_type" not in data:
        return jsonify({"message": "Missing account_type"}), 400

    new_account = add_account(data['account_type'])
    return jsonify(new_account), 201

@bp.route('/<string:account_id>', methods=['PUT'])
def update_account_route(account_id):
    """Memperbarui akun berdasarkan ID"""
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    updated_account = update_account(account_id, data)
    if updated_account:
        return jsonify(updated_account), 200
    return jsonify({"message": "Account not found"}), 404

@bp.route('/<string:account_id>', methods=['DELETE'])
def delete_account_route(account_id):
    """Menghapus akun berdasarkan ID"""
    if delete_account(account_id):
        return jsonify({"message": "Account deleted"}), 200
    return jsonify({"message": "Account not found"}), 404
