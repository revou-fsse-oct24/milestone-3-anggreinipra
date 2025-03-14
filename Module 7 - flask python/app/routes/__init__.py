import logging
from flask import Blueprint, render_template, jsonify, request

# ✅ Import semua Blueprint dari routes lain
from app.routes.accounts import bp as accounts_bp
from app.routes.users import bp as users_bp

# ✅ Import models untuk operasi data
from app.models import (
    get_all_transactions, get_transaction_by_id, add_transaction, get_account_balance
)

# ✅ Buat Blueprint utama
bp = Blueprint('main', __name__)

# ✅ Daftarkan semua sub-Blueprint
bp.register_blueprint(accounts_bp, url_prefix='/accounts')
bp.register_blueprint(users_bp, url_prefix='/users')

# ✅ Konfigurasi logging
logging.basicConfig(level=logging.DEBUG)

# =====================================
# ✅ Middleware untuk validasi JSON
# =====================================
@bp.before_request
def validate_json():
    """Middleware: Cek apakah request memiliki Content-Type JSON"""
    if request.method in ["POST", "PUT"] and not request.is_json:
        return jsonify({"message": "Request must be in JSON format"}), 400

# =====================================
# ✅ HOMEPAGE
# =====================================
@bp.route('/')
def home():
    return render_template('index.html')

# =====================================
# ✅ TRANSACTION MANAGEMENT ENDPOINTS ✅
# =====================================

@bp.route('/transactions', methods=['GET'])
def transactions():
    """Mengambil semua transaksi, bisa difilter dengan account_id, start_date, end_date."""
    try:
        account_id = request.args.get("account_id", type=int)
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        transactions = get_all_transactions(account_id, start_date, end_date)

        # Validasi apakah transaksi ditemukan
        if not transactions:
            return jsonify({"message": "No transactions found"}), 404

        # Hitung total transaksi (deposit +, withdrawal -)
        total_amount = sum(
            t["amount"] if t["transaction_type"] == "deposit" else -t["amount"] 
            for t in transactions
        )

        return jsonify({
            "transactions": transactions,  # Sudah dalam bentuk dict
            "total_amount": total_amount
        }), 200
    except Exception as e:
        logging.error(f"Error fetching transactions: {str(e)}")
        return jsonify({"message": "Error fetching transactions", "error": str(e)}), 500

@bp.route('/transactions/<int:transaction_id>', methods=['GET'])
def transaction(transaction_id):
    """Mengambil transaksi berdasarkan ID."""
    try:
        transaction = get_transaction_by_id(transaction_id)
        if not transaction:
            return jsonify({"message": "Transaction not found"}), 404
        return jsonify(transaction), 200
    except Exception as e:
        logging.error(f"Error retrieving transaction {transaction_id}: {str(e)}")
        return jsonify({"message": "Error retrieving transaction", "error": str(e)}), 500

@bp.route('/transactions', methods=['POST'])
def create_transaction():
    """Membuat transaksi baru (deposit, withdrawal, atau transfer)."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid JSON format"}), 400

        required_fields = ["account_id", "transaction_type", "amount"]
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 400

        account_id = data['account_id']
        transaction_type = data['transaction_type'].lower()
        amount = data['amount']
        recipient_account_id = data.get('recipient_account_id')

        # Validasi tipe transaksi
        valid_types = ["deposit", "withdrawal", "transfer"]
        if transaction_type not in valid_types:
            return jsonify({"message": "Invalid transaction type"}), 400

        # Validasi saldo untuk withdrawal dan transfer
        sender_balance = get_account_balance(account_id)
        if sender_balance is None:
            return jsonify({"message": "Account not found"}), 404

        if transaction_type in ["withdrawal", "transfer"] and sender_balance < amount:
            return jsonify({"message": "Insufficient funds"}), 400

        # Tambahkan transaksi
        result = add_transaction(account_id, transaction_type, amount, recipient_account_id)

        if isinstance(result, dict) and "error" in result:
            return jsonify({"message": result["error"]}), 400

        return jsonify(result), 201

    except Exception as e:
        logging.error(f"Error creating transaction: {str(e)}")
        return jsonify({"message": "Error creating transaction", "error": str(e)}), 500
