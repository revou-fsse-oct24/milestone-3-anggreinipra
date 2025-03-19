import logging
from flask import Blueprint, request, jsonify
from app.models import (
    get_all_accounts,
    get_account_by_number,
    add_account,
    delete_account,
    get_user_by_email,
    get_account_balance,
)

accounts_bp = Blueprint("accounts", __name__)

logging.basicConfig(level=logging.DEBUG)

# ==============================
# ✅ ACCOUNT MANAGEMENT ENDPOINTS
# ==============================

@accounts_bp.route("/", methods=["GET"])
def get_accounts():
    """Mengembalikan semua akun."""
    accounts = get_all_accounts()
    return jsonify(accounts), 200

@accounts_bp.route("/<string:account_number>", methods=["GET"])
def get_account(account_number):
    """Mengembalikan detail akun berdasarkan nomor akun."""
    account = get_account_by_number(account_number)
    if account:
        return jsonify(account), 200
    return jsonify({"error": "Account not found"}), 404

@accounts_bp.route("/", methods=["POST"])
def create_account():
    """Membuat akun baru untuk pengguna."""
    data = request.get_json()

    if not data or "email" not in data or "initial_balance" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    user = get_user_by_email(data["email"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user["account_number"]:
        return jsonify({"error": "User already has an account"}), 400

    try:
        initial_balance = float(data["initial_balance"])
        if initial_balance < 0:
            return jsonify({"error": "Initial balance cannot be negative"}), 400
    except ValueError:
        return jsonify({"error": "Invalid initial_balance format"}), 400

    new_account = add_account(user["user_id"], initial_balance)

    if "error" in new_account:
        return jsonify(new_account), 400

    return jsonify(new_account), 201

@accounts_bp.route("/<string:account_number>", methods=["DELETE"])
def delete_account_route(account_number):
    """Menghapus akun jika saldo 0."""
    balance = get_account_balance(account_number)

    if balance > 0:
        return jsonify({"error": "Cannot delete account with remaining balance"}), 400

    response = delete_account(account_number)

    if "error" in response:
        return jsonify(response), 404

    return jsonify(response), 200
