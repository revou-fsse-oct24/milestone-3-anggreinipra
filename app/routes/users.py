import logging
from flask import Blueprint, request, jsonify
from app.models import (
    get_all_users, get_user_by_email, get_user_by_id, add_user, update_user_profile, delete_user
)

users_bp = Blueprint("users", __name__)

logging.basicConfig(level=logging.DEBUG)

@users_bp.route("/", methods=["GET"])
def get_users():
    """Mengembalikan daftar semua pengguna dari dummy database"""
    users = get_all_users()
    return jsonify(users), 200

@users_bp.route("/<user_id>", methods=["GET"])
def get_user_by_id_route(user_id):
    """Mengambil user berdasarkan ID"""
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

@users_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    result = add_user(username, email, password)

    if "error" in result:
        return jsonify(result), 400

    return jsonify({
        "message": "User registered successfully",
        "user_id": result["user_id"],
        "account_number": result["account_number"],
        "email": result["email"]
    }), 201

@users_bp.route("/me", methods=["GET"])
def get_profile():
    """Mengambil profil user yang sedang login"""
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200

@users_bp.route("/me", methods=["PUT"])
def update_profile():
    """Memperbarui profil user"""
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    data = request.get_json()
    if not data or "new_username" not in data:
        return jsonify({"error": "Missing new_username"}), 400

    updated_user = update_user_profile(user_id, data["new_username"])

    if not updated_user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(updated_user), 200

@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    """Menghapus pengguna berdasarkan user_id"""
    response = delete_user(user_id)
    if "error" in response:
        return jsonify(response), 404
    return jsonify(response), 200
