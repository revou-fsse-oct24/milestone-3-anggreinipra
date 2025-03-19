import logging
from flask import Blueprint, request, jsonify
from app.models import (
    get_all_transactions,
    get_transaction_by_id,
    add_transaction,
    get_account_by_number,
    get_user_by_email,
)

transactions_bp = Blueprint("transactions", __name__)

logging.basicConfig(level=logging.DEBUG)

# ==============================
# ✅ TRANSACTION MANAGEMENT ENDPOINTS
# ==============================

@transactions_bp.route("/", methods=["GET"])
def get_transactions():
    """Mengembalikan daftar transaksi untuk akun tertentu."""
    account_number = request.args.get("account_number")
    if account_number:
        transactions = get_all_transactions(account_number)
    else:
        transactions = get_all_transactions()

    return jsonify(transactions), 200

@transactions_bp.route("/<string:transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    """Mengembalikan detail transaksi berdasarkan ID transaksi."""
    transaction = get_transaction_by_id(transaction_id)
    if transaction:
        return jsonify(transaction), 200
    return jsonify({"error": "Transaction not found"}), 404

@transactions_bp.route("/", methods=["POST"])
def create_transaction():
    """Membuat transaksi baru (deposit, withdrawal, transfer)."""
    data = request.get_json()

    if not data or "account_number" not in data or "transaction_type" not in data or "amount" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    account_number = data["account_number"]
    transaction_type = data["transaction_type"].lower()
    amount = data["amount"]

    if transaction_type not in ["deposit", "withdrawal", "transfer"]:
        return jsonify({"error": "Invalid transaction type"}), 400

    if transaction_type == "transfer" and "recipient_account_number" not in data:
        return jsonify({"error": "Recipient account number required for transfer"}), 400

    # Check if the account exists
    account = get_account_by_number(account_number)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    # For transfers, also check if the recipient account exists
    if transaction_type == "transfer":
        recipient_account_number = data["recipient_account_number"]
        recipient_account = get_account_by_number(recipient_account_number)
        if not recipient_account:
            return jsonify({"error": "Recipient account not found"}), 404

    # Process the transaction
    transaction = add_transaction(account_number, transaction_type, amount, recipient_account_number if transaction_type == "transfer" else None)

    if "error" in transaction:
        return jsonify(transaction), 400

    return jsonify(transaction), 201
