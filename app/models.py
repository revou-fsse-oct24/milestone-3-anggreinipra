import logging
import random
from datetime import datetime
from decimal import Decimal
from werkzeug.security import generate_password_hash

# ✅ Setup logging
logging.basicConfig(level=logging.DEBUG)


# ✅ Model User
class User:
    def __init__(self, id, username, email, password=None, account_number=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.account_number = account_number or self.generate_account_number()

    def generate_account_number(self):
        """Membuat nomor akun unik berdasarkan tahun, bulan, dan angka acak."""
        current_date = datetime.now()
        year_month = current_date.strftime("%y%m")  # Format YYMM
        random_digits = random.randint(100000, 999999)
        return f"{year_month}-{random_digits}"
    
    def to_dict(self):
        """Mengembalikan data user dalam bentuk dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "account_number": self.account_number
        }


# ✅ Model Transaction
class Transaction:
    def __init__(self, id, account_id, amount, transaction_type, recipient_account_id=None, timestamp=None):
        self.id = id
        self.account_id = account_id
        self.amount = Decimal(amount)  # Gunakan Decimal agar lebih presisi
        self.transaction_type = transaction_type  # deposit, withdrawal, transfer
        self.recipient_account_id = recipient_account_id
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self):
        """Mengembalikan data transaksi dalam bentuk dictionary."""
        return {
            "id": self.id,
            "account_id": self.account_id,
            "amount": float(self.amount),  # JSON kompatibel dengan float
            "transaction_type": self.transaction_type,
            "recipient_account_id": self.recipient_account_id,
            "timestamp": self.timestamp  # Format string ISO 8601
        }


# ✅ Dummy Users
users = [
    User(1, 'john_doe', 'john@gmail.com', generate_password_hash('changeme123'), '2101-123456'),
    User(2, 'jane_smith', 'jane@gmail.com', generate_password_hash('changeme456'), '2101-098765'),
    User(3, 'joe_bloggs', 'joe@gmail.com', generate_password_hash('changeme789'), '2101-123098'),
]

# ✅ Dummy Transactions
transactions = [
    Transaction(1, '2101-123456', 1000, 'deposit'),
    Transaction(2, '2101-098765', 500, 'withdrawal'),
    Transaction(3, '2101-123098', 200, 'transfer', '2101-098765'),
    Transaction(4, '2101-123098', 1500, 'deposit')
]

# ✅ Dummy Account Balances
accounts_db = {
    "2101-123456": Decimal(1000.0),
    "2101-098765": Decimal(500.0),
    "2101-123098": Decimal(2000.0),
}


# ✅ Fungsi User Management
def get_all_users():
    return [user.to_dict() for user in users]  

def get_user_by_id(user_id):
    return next((user for user in users if user.id == user_id), None)

def get_user_by_email(email):
    return next((user for user in users if user.email == email), None)

def add_user(username, email, password, account_number=None):
    if get_user_by_email(email):
        return None  # Email sudah terdaftar

    new_id = max([user.id for user in users], default=0) + 1  
    hashed_password = generate_password_hash(password)
    new_account_number = account_number or User(new_id, username, email, hashed_password).generate_account_number()
    
    new_user = User(new_id, username, email, hashed_password, new_account_number)
    users.append(new_user)

    add_account(new_account_number, 0.0)
    
    return new_user.to_dict()  

def update_user_profile(email, data):
    user = get_user_by_email(email)
    if not user:
        return None

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    if "password" in data:
        user.password = generate_password_hash(data["password"])
    
    return user.to_dict()


# ✅ Fungsi Account Management
def get_all_accounts():
    return [{"account_number": acc, "balance": float(balance)} for acc, balance in accounts_db.items()]

def get_account_by_id(account_number):
    return {"account_number": account_number, "balance": float(accounts_db.get(account_number, 0.0))}

def add_account(account_number, initial_balance=0.0):
    if account_number in accounts_db:
        return {"error": "Account already exists"}
    
    accounts_db[account_number] = Decimal(initial_balance)
    return {"account_number": account_number, "balance": float(initial_balance)}

def update_account(account_number, new_balance):
    if account_number not in accounts_db:
        return {"error": "Account not found"}
    
    accounts_db[account_number] = Decimal(new_balance)
    return {"account_number": account_number, "balance": float(new_balance)}

def delete_account(account_number):
    if account_number not in accounts_db:
        return {"error": "Account not found"}
    
    del accounts_db[account_number]
    return {"message": "Account deleted successfully"}

def is_valid_account(account_number):
    return account_number in accounts_db


# ✅ Fungsi Transaction Management
def get_all_transactions(account_id=None, start_date=None, end_date=None):
    filtered_transactions = transactions[:]

    if account_id:
        filtered_transactions = [t for t in filtered_transactions if t.account_id == account_id]

    if start_date and end_date:
        try:
            start_date = datetime.fromisoformat(start_date)
            end_date = datetime.fromisoformat(end_date)
            filtered_transactions = [
                t for t in filtered_transactions 
                if start_date <= datetime.fromisoformat(t.timestamp) <= end_date
            ]
        except ValueError:
            return []

    return [t.to_dict() for t in filtered_transactions]

def get_transaction_by_id(transaction_id):
    transaction = next((t for t in transactions if t.id == transaction_id), None)
    return transaction.to_dict() if transaction else None

def get_account_balance(account_id):
    return float(accounts_db.get(account_id, 0.0))


# ✅ Fungsi untuk menambahkan transaksi
def add_transaction(account_id, amount, transaction_type, recipient_account_id=None):
    if account_id not in accounts_db:
        return {"error": "Account not found"}

    amount = Decimal(amount)
    new_id = max([t.id for t in transactions], default=0) + 1
    transaction = Transaction(new_id, account_id, amount, transaction_type, recipient_account_id)
    
    if transaction_type == "deposit":
        accounts_db[account_id] += amount
    elif transaction_type == "withdrawal":
        if accounts_db[account_id] < amount:
            return {"error": "Insufficient balance"}
        accounts_db[account_id] -= amount
    elif transaction_type == "transfer":
        if recipient_account_id not in accounts_db or accounts_db[account_id] < amount:
            return {"error": "Invalid transfer"}
        accounts_db[account_id] -= amount
        accounts_db[recipient_account_id] += amount

    transactions.append(transaction)
    return transaction.to_dict()
