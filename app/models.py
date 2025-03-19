import hashlib
import uuid

# ===============================
# ✅ DUMMY DATABASE
# ===============================
users_db = []
accounts_db = []
transactions_db = []

# ===============================
# ✅ HELPER FUNCTIONS
# ===============================

def generate_account_number():
    """Membuat nomor rekening unik dengan format 10 digit."""
    return str(uuid.uuid4().int)[:10]

def hash_password(password):
    """Meng-hash password menggunakan SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

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

    user_id = str(uuid.uuid4())
    account_number = None  # Akun dibuat terpisah di accounts.py

    new_user = {
        "user_id": user_id,
        "user_name": username,
        "email": email,
        "account_number": account_number,
        "password": hash_password(password),
    }

    users_db.append(new_user)
    return new_user

def update_user_profile(user_id, new_username=None):
    user = get_user_by_id(user_id)
    if not user:
        return None

    if new_username:
        user["user_name"] = new_username

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
    return accounts_db

def get_account_by_number(account_number):
    return next((acc for acc in accounts_db if acc["account_number"] == account_number), None)

def get_account_balance(account_number):
    account = get_account_by_number(account_number)
    return account["balance"] if account else None

def add_account(user_id, initial_balance):
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

    user["account_number"] = account_number  # Hubungkan akun ke user
    accounts_db.append(new_account)
    return new_account

def delete_account(account_number):
    global accounts_db
    account = get_account_by_number(account_number)

    if not account:
        return {"error": "Account not found"}

    if account["balance"] > 0:
        return {"error": "Cannot delete account with remaining balance"}

    accounts_db = [acc for acc in accounts_db if acc["account_number"] != account_number]

    # Hapus account_number dari user terkait
    user = get_user_by_id(account["user_id"])
    if user:
        user["account_number"] = None

    return {"message": "Account deleted successfully"}

# ===============================
# ✅ TRANSACTION MANAGEMENT
# ===============================

def get_all_transactions(account_number=None):
    if account_number:
        return [tx for tx in transactions_db if tx["account_number"] == account_number]
    return transactions_db

def get_transaction_by_id(transaction_id):
    return next((tx for tx in transactions_db if tx["transaction_id"] == transaction_id), None)

def add_transaction(account_number, transaction_type, amount, recipient_account_number=None):
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

    transaction_id = str(uuid.uuid4())

    transaction = {
        "transaction_id": transaction_id,
        "account_number": account_number,
        "transaction_type": transaction_type,
        "amount": amount,
        "recipient_account_number": recipient_account_number if transaction_type == "transfer" else None,
    }

    transactions_db.append(transaction)

    # Update saldo akun
    if transaction_type == "deposit":
        sender_account["balance"] += amount
    elif transaction_type == "withdrawal":
        sender_account["balance"] -= amount
    elif transaction_type == "transfer":
        sender_account["balance"] -= amount
        recipient_account["balance"] += amount

    return transaction
