from app.models.accounts import Account
from flask import Blueprint, request, jsonify
from app.models.users import User
from app.database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.utils.auth import hash_password, verify_password
from datetime import datetime
from random import randint

users_bp = Blueprint('users', __name__, url_prefix="/users")

# Helper: Generate user_id sequentially
def generate_user_id():
    last_user = User.query.order_by(User.id.desc()).first()
    if last_user and last_user.user_id:
        return f"{int(last_user.user_id) + 1:03d}"
    return "001"

# Helper: Generate unique account number
def generate_account_number():
    date_part = datetime.now().strftime("%d%m%y")
    random_part = randint(100000, 999999)
    return f"{date_part}-{random_part}"

# POST /users → Register a new user
@users_bp.route('', methods=['POST'])
def register_user():
    data = request.get_json()
    required_fields = ['user_name', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    hashed_pw = hash_password(data['password'])
    new_user = User(
        user_name=data['user_name'],
        email=data['email'],
        password=hashed_pw,
        user_id=generate_user_id(),
        account_number=generate_account_number() 
    )

    db.session.add(new_user)
    db.session.commit()

    # Tambahkan akun baru yang terhubung dengan user baru
    new_account = Account(
        user_id=new_user.user_id,
        account_number=generate_account_number(),
        balance=0.0,
        account_type='basic', 
        created_at=datetime.utcnow()
    )
    db.session.add(new_account)
    db.session.commit()

    token = create_access_token(identity=new_user.email)
    return jsonify({
        'message': 'User registered successfully',
        'access_token': token,
        'user': new_user.to_dict()
    }), 201


# GET /token
@users_bp.route('/get_token', methods=['GET'])
@jwt_required()
def get_token():
    # Dapatkan email dari token JWT yang terautentikasi
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Buat token lagi untuk user yang sama
    token = create_access_token(identity=user.email)
    return jsonify({'access_token': token}), 200

# GET /users → Retrieve all users
@users_bp.route('', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# GET /users/<user_id> → Retrieve specific user
@users_bp.route('/<string:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

# GET /users/me → Retrieve currently logged-in user profile
@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_my_profile():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

# PUT /users/me → Update currently logged-in user profile
@users_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_my_profile():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if 'user_name' in data:
        user.user_name = data['user_name']
    if 'password' in data:
        user.password = hash_password(data['password'])

    db.session.commit()
    return jsonify({'message': 'User profile updated'}), 200
