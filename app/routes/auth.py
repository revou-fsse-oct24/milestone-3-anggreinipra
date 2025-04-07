from flask import Blueprint, request, jsonify
from app.models.users import User
from app.database import db
from app.utils.auth import verify_password
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='')

# POST /auth/login → User login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password):
        return jsonify({'error': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=user.email)
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'user_id': user.user_id,
            'user_name': user.user_name,
            'email': user.email,
            'account_number': user.account_number,
            'created_at': str(user.created_at)
        }
    }), 200
