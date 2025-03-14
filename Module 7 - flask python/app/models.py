from werkzeug.security import generate_password_hash
import random
from datetime import datetime
from decimal import Decimal

# ✅ Model User
class User:
    def __init__(self, id, username, email, password=None, account_number=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.account_number = account_number or self.generate_account_number()

    def generate_account_number(self):
        current_date = datetime.now()
        year_month = current_date.strftime("%y%m")  # Format YYMM
        random_digits = random.randint(100000, 999999)
        return f"{year_month}-{random_digits}"
    
    def to_dict(self):
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

# ✅ Fungsi untuk mengecek apakah akun valid
def is_valid_account(account_number):
    """Memeriksa apakah account_number ada di dalam accounts_db."""
    return account_number in accounts_db

# ✅ Fungsi User Management
def get_all_users():
    """Mengembalikan daftar semua user sebagai daftar objek User."""
    return users  

def get_user_by_id(user_id):
    """Mengambil user berdasarkan ID."""
    return next((user for user in users if user.id == user_id), None)

def get_user_by_email(email):
    """Mengambil user berdasarkan email."""
    return next((user for user in users if user.email == email), None)

def add_user(username, email, password, account_number=None):
    """Menambahkan user baru, menghindari email yang sudah ada."""
    if get_user_by_email(email):
        return None  

    new_id = max([user.id for user in users], default=0) + 1  
    hashed_password = generate_password_hash(password)
    new_account_number = account_number or User(new_id, username, email, hashed_password).generate_account_number()
    
    new_user = User(new_id, username, email, hashed_password, new_account_number)
    users.append(new_user)

    # Set initial balance to zero
    accounts_db[new_account_number] = Decimal(0.0)
    
    return new_user  

def delete_user(user_id):
    """Menghapus user berdasarkan ID."""
    global users
    user_to_delete = get_user_by_id(user_id)
    if user_to_delete:
        users = [user for user in users if user.id != user_id]
        return True  
    return False  

def update_user_by_id(user_id, username=None, password=None):
    """Memperbarui informasi user."""
    user = get_user_by_id(user_id)
    if user:
        if username:
            user.username = username
        if password:
            user.password = generate_password_hash(password) 
        return user  
    return None  

# ✅ Fungsi Transaction Management
def get_all_transactions(account_id=None, start_date=None, end_date=None):
    """Mengambil semua transaksi, dengan filter opsional berdasarkan account_id, start_date, dan end_date."""
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

    return filtered_transactions  

def get_transaction_by_id(transaction_id):
    """Mengambil transaksi berdasarkan ID."""
    return next((t for t in transactions if t.id == transaction_id), None)

def get_account_balance(account_id):
    """Mengambil saldo akun."""
    return float(accounts_db.get(account_id, 0.0))  

def add_transaction(account_id, transaction_type, amount, recipient_account_id=None):
    """Menambahkan transaksi baru dengan validasi yang ketat."""
    amount = Decimal(amount)
    if not is_valid_account(account_id):
        return {"error": "Sender account not found"}

    sender_balance = accounts_db[account_id]

    # ✅ Validasi transaksi transfer
    if transaction_type == "transfer":
        if not is_valid_account(recipient_account_id):
            return {"error": "Recipient account not found"}
        if sender_balance < amount:
            return {"error": "Insufficient balance"}

    # ✅ Validasi transaksi penarikan
    elif transaction_type == "withdrawal":
        if sender_balance < amount:
            return {"error": "Insufficient balance"}

    # ✅ Buat transaksi baru
    new_id = max([t.id for t in transactions], default=0) + 1
    new_transaction = Transaction(new_id, account_id, amount, transaction_type, recipient_account_id)

    # ✅ Update saldo akun
    if transaction_type == "deposit":
        accounts_db[account_id] += amount
    elif transaction_type == "withdrawal":
        accounts_db[account_id] -= amount
    elif transaction_type == "transfer":
        accounts_db[account_id] -= amount
        accounts_db[recipient_account_id] += amount

    transactions.append(new_transaction)
    return new_transaction  

def get_total_transaction_amount(account_id):
    """Menghitung total saldo akhir dari semua transaksi untuk account_id tertentu."""
    total_amount = sum(
        t.amount if t.transaction_type == "deposit" else -t.amount
        for t in transactions if t.account_id == account_id
    )

    return float(total_amount)