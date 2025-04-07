from flask import Blueprint, request, jsonify
from app.models.users import User
from app.database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.utils.auth import hash_password, verify_password, token_required, generate_token

users_bp = Blueprint('users', __name__)

# POST /users → Register a new user
@users_bp.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    required_fields = ['user_name', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    hashed_pw = hash_password(data['password'])
    new_user = User(user_name=data['user_name'], email=data['email'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    token = create_access_token(identity=new_user.email)
    return jsonify({'message': 'User registered successfully', 'access_token': token}), 201


# GET /users → Retrieve all users
@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


# GET /users/<user_id> → Retrieve specific user
@users_bp.route('/users/<string:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


# GET /users/me → Retrieve currently logged-in user profile
@users_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_my_profile():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


# PUT /users/me → Update currently logged-in user profile
@users_bp.route('/users/me', methods=['PUT'])
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
