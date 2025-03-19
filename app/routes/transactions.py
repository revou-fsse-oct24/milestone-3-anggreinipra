from flask import Blueprint, request, jsonify
import logging
from app.models import (
    get_all_transactions, 
    get_transaction_by_id, 
    add_transaction, 
    get_total_transaction_amount, 
    is_valid_account
)

bp = Blueprint('transactions', __name__)
logging.basicConfig(level=logging.DEBUG)

@bp.route('/', methods=['GET'])
def get_transactions():
    """Mengambil semua transaksi dengan filter opsional berdasarkan account_id."""
    try:
        account_id = request.args.get("account_id")

        # ✅ Pastikan akun valid sebelum mencari transaksi
        if account_id and not is_valid_account(account_id):
            return jsonify({"message": "Account not found"}), 404

        transactions = get_all_transactions(account_id)
        
        total_amount = get_total_transaction_amount(account_id) if account_id else None

        return jsonify({
            "transactions": [t.to_dict() for t in transactions],
            "total_amount": total_amount  # Menampilkan total saldo akhir jika ada filter account_id
        })
    except Exception as e:
        logging.error(f"Error fetching transactions: {str(e)}")
        return jsonify({"message": "Error fetching transactions", "error": str(e)}), 500

@bp.route('/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    """Mengambil detail transaksi berdasarkan ID."""
    try:
        transaction = get_transaction_by_id(transaction_id)
        if transaction:
            return jsonify(transaction.to_dict())
        return jsonify({"message": "Transaction not found"}), 404
    except Exception as e:
        logging.error(f"Error retrieving transaction {transaction_id}: {str(e)}")
        return jsonify({"message": "Error retrieving transaction", "error": str(e)}), 500

@bp.route('/', methods=['POST'])
def create_transaction():
    """Membuat transaksi baru (deposit, withdrawal, transfer)."""
    try:
        data = request.get_json()

        # ✅ Validasi input
        required_fields = ["account_id", "transaction_type", "amount"]
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 400

        account_id = data['account_id']
        transaction_type = data['transaction_type'].lower()
        amount = float(data['amount'])  # ✅ Pastikan amount bertipe float
        recipient_account_id = data.get('recipient_account_id')

        # ✅ Validasi akun pengirim
        if not is_valid_account(account_id):
            return jsonify({"message": "Sender account not found"}), 404

        # ✅ Validasi jenis transaksi
        valid_types = ["deposit", "withdrawal", "transfer"]
        if transaction_type not in valid_types:
            return jsonify({"message": "Invalid transaction type"}), 400

        # ✅ Jika transaksi adalah transfer, pastikan recipient_account_id valid
        if transaction_type == "transfer":
            if not recipient_account_id:
                return jsonify({"message": "Recipient account number is required for transfers"}), 400

            if not is_valid_account(recipient_account_id):
                return jsonify({"message": "Recipient account not found"}), 404

        # ✅ Jalankan transaksi
        new_transaction = add_transaction(account_id, transaction_type, amount, recipient_account_id)

        if isinstance(new_transaction, dict) and "error" in new_transaction:
            return jsonify({"message": new_transaction["error"]}), 400

        return jsonify(new_transaction.to_dict()), 201
    except Exception as e:
        logging.error(f"Error creating transaction: {str(e)}")
        return jsonify({"message": "Error creating transaction", "error": str(e)}), 500