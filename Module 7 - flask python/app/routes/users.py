from flask import Blueprint, request, jsonify
from app.models import get_user_by_email, add_user, get_user_by_id
from app.utils.auth import hash_password, check_password

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
    return jsonify({"message": "Login functionality removed"}), 404