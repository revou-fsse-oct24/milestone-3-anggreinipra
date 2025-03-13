from flask_bcrypt import Bcrypt # type: ignore
from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import timedelta

bcrypt = Bcrypt()

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.check_password_hash(hashed, password)

def generate_token(user_id):
    return create_access_token(identity=user_id, expires_delta=timedelta(days=1))
