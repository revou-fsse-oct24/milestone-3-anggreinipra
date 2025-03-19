import hashlib
import uuid
from datetime import datetime
from flask import jsonify

# ===============================
# ✅ DUMMY DATABASE
# ===============================
users_db = []
accounts_db = []
transactions_db = []

# ===============================
# ✅ HELPER FUNCTIONS
# ===============================

def generate_user_id():
    """Membuat user_id berurutan mulai dari 001."""
    if not users_db:
        return "001"
    last_id = int(users_db[-1]["user_id"]) 
    new_id = f"{last_id + 1:03d}"
    return new_id

def generate_account_number():
    """Membuat nomor rekening unik dengan format 10 digit."""
    return str(uuid.uuid4().int)[:10]

def hash_password(password):
    """Meng-hash password menggunakan SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

# ===============================
# ✅ DUMMY DATA UNTUK TESTING
# ===============================

users_db.extend([
    {
        "user_id": "001",
        "user_name": "Layla",
        "email": "laylamm@gmail.com",
        "account_number": "4338761761",
        "password": hash_password("Layla123"),
    },
    {
        "user_id": "002",
        "user_name": "Ari",
        "email": "ari@gmail.com",
        "account_number": "5239876543",
        "password": hash_password("AriPass"),
    },
    {
        "user_id": "003",
        "user_name": "Nadia",
        "email": "nadia@gmail.com",
        "account_number": "7894561230",
        "password": hash_password("Nadia321"),
    }
])

accounts_db = [
    {
        "account_number": "4338761761",
        "user_id": "001",
        "balance": 5000,
        "account_name": "Tabungan Layla",
        "account_type": "savings",
        "status": "active"
    },
    {
        "account_number": "5239876543",
        "user_id": "002",
        "balance": 10000,
        "account_name": "Rekening Bisnis Ari",
        "account_type": "business",
        "status": "active"
    },
    {
        "account_number": "7894561230",
        "user_id": "003",
        "balance": 7500,
        "account_name": "Dana Darurat Nadia",
        "account_type": "savings",
        "status": "inactive"
    },
    {
        "account_number": "9999999999",
        "user_id": "004",
        "balance": 0,
        "account_name": "Testing Account untuk delete",
        "account_type": "savings",
        "status": "inactive"
    }
]

transactions_db = [
    {
        "transaction_id": "txn001",
        "account_number": "4338761761",
        "transaction_type": "deposit",
        "amount": 5000,
        "recipient_account_number": None,
        "date_transaction": "2025-03-19T15:30:00",
        "balance": 10000
    },
    {
        "transaction_id": "txn002",
        "account_number": "5239876543",
        "transaction_type": "withdrawal",
        "amount": 2000,
        "recipient_account_number": None,
        "date_transaction": "2025-03-19T16:00:00",
        "balance": 8000
    },
    {
        "transaction_id": "txn003",
        "account_number": "4338761761",
        "transaction_type": "transfer",
        "amount": 1000,
        "recipient_account_number": "5239876543",
        "date_transaction": "2025-03-19T17:00:00",
        "balance": 9000
    },
    {
        "transaction_id": "txn004",
        "account_number": "5239876543",
        "transaction_type": "transfer",
        "amount": 1000,
        "recipient_account_number": None,
        "date_transaction": "2025-03-19T17:00:00",
        "balance": 9000
    },
    # 🔹 Transaksi untuk Nadia
    {
        "transaction_id": "txn005",
        "account_number": "7894561230",  # Akun Nadia
        "transaction_type": "deposit",
        "amount": 3000,
        "recipient_account_number": None,
        "date_transaction": "2025-03-19T18:00:00",
        "balance": 10500  # 7500 + 3000 deposit
    },
    {
        "transaction_id": "txn006",
        "account_number": "7894561230",  # Akun Nadia melakukan transfer
        "transaction_type": "transfer",
        "amount": 1500,
        "recipient_account_number": "5239876543",  # Transfer ke Ari
        "date_transaction": "2025-03-19T19:00:00",
        "balance": 9000  # 10500 - 1500 transfer
    },
    {
        "transaction_id": "txn007",
        "account_number": "5239876543",  # Akun Ari menerima dari Nadia
        "transaction_type": "transfer",
        "amount": 1500,
        "recipient_account_number": None,
        "date_transaction": "2025-03-19T19:00:00",
        "balance": 10500  # 9000 + 1500 transfer masuk dari Nadia
    }
]


# ===============================
# ✅ USER MANAGEMENT
# ===============================

def get_all_users():
    return users_db

def get_user_by_id(user_id):
    return next((user for user in users_db if user["user_id"] == user_id), None)

def get_user_by_email(email):
    return next((user for user in users_db if user["email"] == email), None)

def add_user(username, email, password):
    if get_user_by_email(email):
        return {"error": "Email already registered"}

    user_id = generate_user_id()
    account_number = generate_account_number()

    new_user = {
        "user_id": user_id,
        "user_name": username,
        "email": email,
        "account_number": account_number,
        "password": hash_password(password),
    }
    users_db.append(new_user)

    new_account = {
        "account_number": account_number,
        "user_id": user_id,
        "balance": 0,
    }
    accounts_db.append(new_account)

    return new_user


def update_user_profile(user_id, user_name=None, email=None, password=None):
    """Memperbarui profil user berdasarkan user_id"""
    user = get_user_by_id(user_id)
    if not user:
        return None

    if user_name:
        user["user_name"] = user_name

    if email:
        if any(u["email"] == email and u["user_id"] != user_id for u in users_db):
            return {"error": "Email is already in use"}

        user["email"] = email

    if password:
        user["password"] = hash_password(password)

    return user

def delete_user(user_id):
    global users_db
    user = get_user_by_id(user_id)

    if not user:
        return {"error": "User not found"}

    if user["account_number"]:
        return {"error": "Cannot delete user with an active account"}

    users_db = [u for u in users_db if u["user_id"] != user_id]
    return {"message": "User deleted successfully"}

# ===============================
# ✅ ACCOUNT MANAGEMENT
# ===============================

def get_all_accounts():
    """Mengambil semua akun dengan informasi user terkait."""
    account_list = []

    for account in accounts_db:
        user = get_user_by_id(account["user_id"]) 
        account_list.append({
            "user_id": account["user_id"],
            "username": user["user_name"] if user else None,
            "email": user["email"] if user else None,
            "account_number": account["account_number"],
            "balance": account["balance"]
        })

    return account_list


def get_account_by_number(account_number):
    return next((acc for acc in accounts_db if acc["account_number"] == account_number), None)

def get_account_balance(account_number):
    account = get_account_by_number(account_number)
    return account["balance"] if account else None

def add_account(user_id, initial_balance):
    """Menambahkan akun untuk user yang sudah ada."""
    user = get_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}

    if user["account_number"]:
        return {"error": "User already has an account"}

    account_number = generate_account_number()
    new_account = {
        "account_number": account_number,
        "user_id": user_id,
        "balance": initial_balance,
    }

    user["account_number"] = account_number
    accounts_db.append(new_account)
    return new_account

def update_account(account_number, new_balance):
    """Memperbarui saldo akun berdasarkan nomor rekening."""
    account = get_account_by_number(account_number)

    if not account:
        return {"error": "Account not found"}

    if new_balance < 0:
        return {"error": "Balance cannot be negative"}

    account["balance"] = new_balance
    return {
        "message": "Account balance updated successfully",
        "account_number": account["account_number"],
        "balance": account["balance"]
    }


def delete_account(account_number):
    global accounts_db
    account = get_account_by_number(account_number)

    if not account:
        return {"error": "Account not found"}

    if account["balance"] > 0:
        return {"error": "Cannot delete account with remaining balance"}

    accounts_db = [acc for acc in accounts_db if acc["account_number"] != account_number]

    user = get_user_by_id(account["user_id"])
    if user:
        user["account_number"] = None

    return {"message": "Account deleted successfully"}

# ===============================
# ✅ TRANSACTION MANAGEMENT
# ===============================

def add_transaction(account_number, transaction_type, amount, recipient_account_number=None):
    """Menambahkan transaksi baru dan mengupdate saldo akun."""
    sender_account = get_account_by_number(account_number)

    if not sender_account:
        return {"error": "Sender account not found"}

    if transaction_type == "withdrawal" and sender_account["balance"] < amount:
        return {"error": "Insufficient balance"}

    if transaction_type == "transfer":
        recipient_account = get_account_by_number(recipient_account_number)
        if not recipient_account:
            return {"error": "Recipient account not found"}
        if recipient_account_number == account_number:
            return {"error": "Cannot transfer to the same account"}

    # ✅ Buat timestamp untuk transaksi
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transaction_id = f"txn{len(transactions_db) + 1:03d}"

    # Update balance
    if transaction_type == "deposit":
        sender_account["balance"] += amount
    elif transaction_type == "withdrawal":
        sender_account["balance"] -= amount
    elif transaction_type == "transfer":
        sender_account["balance"] -= amount
        recipient_account["balance"] += amount

    transaction = {
        "transaction_id": transaction_id,
        "account_number": account_number,
        "transaction_type": transaction_type,
        "amount": amount,
        "recipient_account_number": recipient_account_number if transaction_type == "transfer" else None,
        "date_transaction": timestamp,
        "balance": sender_account["balance"]
    }

    transactions_db.append(transaction)
    return transaction


def get_all_transactions(account_number=None):
    """Mengambil semua transaksi dengan informasi user dan saldo setelah transaksi."""
    filtered_transactions = transactions_db

    if account_number:
        filtered_transactions = [tx for tx in transactions_db if tx["account_number"] == account_number]

    result = []
    for tx in filtered_transactions:
        user = get_user_by_id(get_account_by_number(tx["account_number"])["user_id"])

        result.append({
            "username": user["user_name"] if user else None,
            "user_id": user["user_id"] if user else None,
            "transaction_id": tx["transaction_id"],
            "account_number": tx["account_number"],
            "transaction_type": tx["transaction_type"],
            "amount": tx["amount"],
            "recipient_account_number": tx["recipient_account_number"],
            "date_transaction": tx.get("date_transaction", "N/A"),
            "balance": tx["balance"]
        })

    return result


def get_transaction_by_id(transaction_id):
    """Mengambil detail transaksi berdasarkan transaction_id."""
    tx = next((t for t in transactions_db if t["transaction_id"] == transaction_id), None)
    if not tx:
        return {"error": "Transaction not found"}

    account = get_account_by_number(tx["account_number"])
    if not account:
        return {"error": f"Account not found for transaction {transaction_id}, account_number: {tx['account_number']}"}

    user = get_user_by_id(account["user_id"])
    if not user:
        return {"error": f"User not found for account {account['account_number']}"}

    return {
        "transaction_id": tx["transaction_id"],
        "account_number": tx["account_number"],
        "user_id": user["user_id"],
        "username": user["user_name"],
        "transaction_type": tx["transaction_type"],
        "amount": tx["amount"],
        "recipient_account_number": tx.get("recipient_account_number"),
        "date_transaction": tx["date_transaction"], 
        "balance": tx["balance"]
    }


def get_transactions_by_account(account_number):
    """Mengambil daftar transaksi berdasarkan account_number."""
    transactions = [tx for tx in transactions_db if tx["account_number"] == account_number]

    if not transactions:
        return jsonify({"error": "No transactions found for this account"}), 404

    return jsonify(transactions), 200