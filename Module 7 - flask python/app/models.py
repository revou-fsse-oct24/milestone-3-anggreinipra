from werkzeug.security import generate_password_hash
import random
from datetime import datetime

class User:
    def __init__(self, id, username, email, password=None, account_number=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.account_number = account_number or self.generate_account_number()  # Generate account number if None
        
    def generate_account_number(self):
        current_date = datetime.now()
        year_month = current_date.strftime("%y%m")  # Format YYMM
        random_digits = random.randint(100000, 999999) 
        return f"{year_month}-{random_digits}"


# Database dummy 
users = [
    User(1, 'john_doe', 'john@gmail.com', generate_password_hash('changeme123'), '2101-123456'),
    User(2, 'jane_smith', 'jane@gmail.com', generate_password_hash('changeme456'), '2101-098765'),
    User(3, 'joe_bloggs', 'joe@gmail.com', generate_password_hash('changeme789'), '2101-123098'),
]

def get_all_users():
    return users

def get_user_by_id(user_id):
    return next((user for user in users if user.id == user_id), None)

def get_user_by_email(email):
    return next((user for user in users if user.email == email), None)

def add_user(username, email, password, account_number=None):
    new_id = len(users) + 1
    hash_password = generate_password_hash(password)
    new_account_number = account_number or User(new_id, username, email, hash_password).generate_account_number()
    new_user = User(new_id, username, email, hash_password, new_account_number)
    users.append(new_user)
    return new_user

# update user based on id
def delete_user(user_id):
    global users
    users = [user for user in users if user.id != user_id]
    return True

# update user based on email
def update_user_by_email(email, username=None, password=None):
    user = get_user_by_email(email)
    if user:
        if username:
            user.username = username
        if password:
            user.password = generate_password_hash(password) 
        return user
    return None