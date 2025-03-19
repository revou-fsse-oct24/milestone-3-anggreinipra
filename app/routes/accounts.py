import logging
from flask import Blueprint, request, jsonify
from app.models import (
    get_all_accounts,
    get_account_by_number,
    delete_account,
    get_user_by_email,
    get_account_balance,
    get_user_by_id
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

        return jsonify([formatted_account]), 200 

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

@accounts_bp.route("/<account_number>", methods=["PUT"])
def update_account(account_number):
    """Memperbarui informasi akun (tanpa mengubah saldo)"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    account = get_account_by_number(account_number)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    # Update hanya field yang valid (tanpa balance)
    allowed_fields = {"account_name", "account_type", "status"}
    updated_fields = {key: value for key, value in data.items() if key in allowed_fields}

    if not updated_fields:
        return jsonify({"error": "No valid fields to update"}), 400

    account.update(updated_fields)

    return jsonify({
        "message": "Account updated successfully",
        "account": account
    }), 200


@accounts_bp.route("/<account_number>", methods=["DELETE"])
def delete_account_by_number(account_number):
    """Menghapus akun jika saldo 0 dan mendapat konfirmasi dari user"""
    account = get_account_by_number(account_number)

    if not account:
        return jsonify({"error": "Account not found"}), 404

    if account["balance"] > 0:
        return jsonify({
            "error": "Cannot delete account",
            "message": "The account still has a balance, deletion is not allowed."
        }), 400

    # Konfirmasi tambahan
    confirmation = request.args.get("confirm")
    if confirmation != "yes":
        return jsonify({
            "message": "Are you sure you want to delete this account? This action cannot be undone.",
            "hint": "Add ?confirm=yes to the request URL to proceed."
        }), 400

    # Hapus akun
    delete_account(account_number)

    return jsonify({"message": "Account deleted successfully"}), 200
