import datetime
from functools import wraps
from flask import request, jsonify, current_app
import jwt
import bcrypt
from app.models.users import User
from app.database import db

# ------------------------
# Password Hashing Utils
# ------------------------

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# ------------------------
# JWT Auth Utils
# ------------------------

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_current_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    try:
        token = auth_header.split(" ")[1]
        user_id = decode_token(token)
        if user_id:
            user = db.session.query(User).filter_by(user_id=user_id).first()
            return user
        return None
    except IndexError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'message': 'Token is missing or invalid'}), 401
        return f(current_user=user, *args, **kwargs)
    return decorated
