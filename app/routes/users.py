from flask import Blueprint, request, jsonify
from app.models import User, db
from werkzeug.security import generate_password_hash

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.__dict__ for user in users]), 200

@users_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    user = User(
        user_id=data['user_id'],
        user_name=data['username'],
        email=data['email'],
        password=hashed_password,
        account_number=data['account_number']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201
