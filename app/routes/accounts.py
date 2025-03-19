import logging
from flask import Blueprint, request, jsonify
from app.models import (
    get_all_accounts,
    get_account_by_number,
    add_account,
    delete_account,
    get_user_by_email,
    get_account_balance,
    get_user_by_id,
)

accounts_bp = Blueprint("accounts", __name__)

logging.basicConfig(level=logging.DEBUG)

# ==============================
# ✅ ACCOUNT MANAGEMENT ENDPOINTS
# ==============================

@accounts_bp.route("/", methods=["GET"])
def get_accounts():
    """Mengambil semua akun atau akun berdasarkan email."""
    email = request.args.get("email")

    if email:
        user = get_user_by_email(email)
        if not user:
            return jsonify({"error": "User not found"}), 404

        account = get_account_by_number(user["account_number"])
        if not account:
            return jsonify({"error": "Account not found"}), 404

        # Format data akun agar menyertakan informasi user
        formatted_account = {
            "user_id": user["user_id"],
            "username": user["user_name"],
            "email": user["email"],
            "account_number": account["account_number"],
            "balance": account["balance"]
        }

        return jsonify(formatted_account), 200

    return jsonify(get_all_accounts()), 200

@accounts_bp.route("/<account_number>", methods=["GET"])
def get_account_by_account_number(account_number):
    """Mengambil informasi akun berdasarkan account_number."""
    account = get_account_by_number(account_number)
    
    if not account:
        return jsonify({"error": "Account not found"}), 404

    user = get_user_by_id(account["user_id"])
    
    account_data = {
        "user_id": account["user_id"],
        "username": user["user_name"] if user else None,
        "email": user["email"] if user else None,
        "account_number": account["account_number"],
        "balance": account["balance"]
    }

    return jsonify(account_data), 200


@accounts_bp.route("/", methods=["POST"])
def create_account():
    """Membuat akun baru untuk pengguna jika belum memiliki akun."""
    data = request.get_json()

    # Validasi input
    if not data or "email" not in data or "initial_balance" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    user = get_user_by_email(data["email"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Cek apakah user sudah memiliki akun
    if user["account_number"]:
        return jsonify({
            "error": "User already has an account",
            "account_number": user["account_number"]
        }), 400

    try:
        initial_balance = float(data["initial_balance"])
        if initial_balance < 0:
            return jsonify({"error": "Initial balance cannot be negative"}), 400
    except ValueError:
        return jsonify({"error": "Invalid initial_balance format"}), 400

    # Buat akun baru
    new_account = add_account(user["user_id"], initial_balance)

    if "error" in new_account:
        return jsonify(new_account), 400

    return jsonify({
        "message": "Account created successfully",
        "account_number": new_account["account_number"],
        "balance": new_account["balance"]
    }), 201
    
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
