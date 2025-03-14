import logging
from flask import Blueprint, render_template, jsonify, request
from app.models import (
    get_all_users,
    get_user_by_id,
    get_user_by_email,
    add_user,
    delete_user,
    update_user_by_id,
    get_all_transactions,
    get_transaction_by_id,
    add_transaction,
    get_account_balance
)
from app.utils.auth import hash_password

bp = Blueprint('main', __name__)
logging.basicConfig(level=logging.DEBUG)

# ✅ Homepage
@bp.route('/')
def home():
    return render_template('index.html')

# =====================================
# ✅ USER MANAGEMENT ENDPOINTS ✅
# =====================================

@bp.route('/users', methods=['GET'])
def users():
    try:
        all_users = get_all_users()
        return jsonify([user.to_dict() for user in all_users]), 200
    except Exception as e:
        logging.error(f"Error fetching users: {str(e)}")
        return jsonify({"message": "Error fetching users", "error": str(e)}), 500

@bp.route('/users/<int:user_id>', methods=['GET'])
def user(user_id):
    try:
        user = get_user_by_id(user_id)
        if user:
            return jsonify(user.to_dict()), 200
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        logging.error(f"Error retrieving user {user_id}: {str(e)}")
        return jsonify({"message": "Error retrieving user", "error": str(e)}), 500

@bp.route('/users', methods=['POST'])
def add_new_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid JSON format"}), 400

        required_fields = ["username", "email", "password"]
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 400

        username = data['username']
        email = data['email']
        password = data['password']

        # Cek apakah email sudah digunakan
        if get_user_by_email(email):
            return jsonify({"message": "Email already exists"}), 400

        new_user = add_user(username, email, password)
        if not new_user:
            return jsonify({"message": "Failed to create user"}), 500

        return jsonify(new_user.to_dict()), 201

    except Exception as e:
        logging.error(f"Error creating user: {str(e)}")
        return jsonify({"message": "Error creating user", "error": str(e)}), 500

@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    try:
        user = get_user_by_id(user_id)
        if user:
            delete_user(user_id)
            return jsonify({"message": "User successfully deleted"}), 200
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        logging.error(f"Error deleting user {user_id}: {str(e)}")
        return jsonify({"message": "Error deleting user", "error": str(e)}), 500

@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400

        username = data.get('username')
        password = data.get('password')

        if password:
            password = hash_password(password)

        updated_user = update_user_by_id(user_id, username, password)
        if updated_user:
            return jsonify(updated_user.to_dict()), 200
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        logging.error(f"Error updating user {user_id}: {str(e)}")
        return jsonify({"message": "Error updating user", "error": str(e)}), 500

# =====================================
# ✅ TRANSACTION MANAGEMENT ENDPOINTS ✅
# =====================================

@bp.route('/transactions', methods=['GET'])
def transactions():
    try:
        account_id = request.args.get("account_id")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        transactions = get_all_transactions(account_id, start_date, end_date)
        
        total_amount = sum(t.amount if t.transaction_type == "deposit" else -t.amount for t in transactions)

        return jsonify({
            "transactions": [t.to_dict() for t in transactions],
            "total_amount": total_amount
        }), 200
    except Exception as e:
        logging.error(f"Error fetching transactions: {str(e)}")
        return jsonify({"message": "Error fetching transactions", "error": str(e)}), 500

@bp.route('/transactions/<int:transaction_id>', methods=['GET'])
def transaction(transaction_id):
    try:
        transaction = get_transaction_by_id(transaction_id)
        if transaction:
            return jsonify(transaction.to_dict()), 200
        return jsonify({"message": "Transaction not found"}), 404
    except Exception as e:
        logging.error(f"Error retrieving transaction {transaction_id}: {str(e)}")
        return jsonify({"message": "Error retrieving transaction", "error": str(e)}), 500

@bp.route('/transactions', methods=['POST'])
def create_transaction():
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

        # Validasi saldo
        sender_balance = get_account_balance(account_id)
        if sender_balance is None:
            return jsonify({"message": "Account not found"}), 404

        result = add_transaction(account_id, transaction_type, amount, recipient_account_id)

        if isinstance(result, dict) and "error" in result:
            return jsonify({"message": result["error"]}), 400

        return jsonify(result.to_dict()), 201

    except Exception as e:
        logging.error(f"Error creating transaction: {str(e)}")
        return jsonify({"message": "Error creating transaction", "error": str(e)}), 500