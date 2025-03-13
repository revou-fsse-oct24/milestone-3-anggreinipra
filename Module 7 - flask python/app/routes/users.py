from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import get_user_by_email, add_user, get_user_by_id
from app.utils.auth import hash_password, check_password, generate_token

bp = Blueprint('users', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if get_user_by_email(data['email']):
        return jsonify({"message": "Email already registered"}), 400

    new_user = add_user(data['username'], data['email'], hash_password(data['password']))
    return jsonify({
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "account_number": new_user.account_number
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = get_user_by_email(data['email'])
    if not user or not check_password(data['password'], user.password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = generate_token(user.id)
    return jsonify({"token": token})

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "account_number": user.account_number
    })
