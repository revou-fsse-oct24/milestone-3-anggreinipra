import logging
import re
from flask import Blueprint, request, jsonify
from app.models import get_user_by_email, add_user, get_user_by_id, update_user_profile  # Mengganti update_user_by_id
from app.utils.auth import hash_password, authenticate_user

bp = Blueprint("users", __name__, url_prefix="/users")

# ✅ Setup logging
logging.basicConfig(level=logging.DEBUG)


# =====================================
# ✅ USER MANAGEMENT ENDPOINTS ✅
# =====================================

@bp.route("/register", methods=["POST"])
def register():
    """Registrasi pengguna baru"""
    try:
        data = request.get_json(silent=True)
        logging.debug(f"Received registration data: {data}")

        # ✅ Validasi request body
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        required_fields = ["username", "email", "password"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        username = data["username"].strip()
        email = data["email"].strip()
        password = data["password"].strip()

        # ✅ Validasi format email
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            return jsonify({"error": "Invalid email format"}), 400

        # ✅ Validasi panjang password
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long"}), 400

        # ✅ Cek apakah email sudah terdaftar
        if get_user_by_email(email):
            return jsonify({"error": "Email already registered"}), 400

        # ✅ Hash password & buat user baru
        hashed_password = hash_password(password)
        new_user = add_user(username, email, hashed_password)

        if not new_user:
            return jsonify({"error": "Failed to register user"}), 500

        logging.debug(f"New user created: {new_user}")

        return jsonify(new_user.to_dict()), 201

    except Exception as e:
        logging.error(f"Error registering user: {str(e)}")
        return jsonify({"error": "Error registering user", "details": str(e)}), 500


@bp.route("/me", methods=["GET"])
def get_profile():
    """Mengambil profil user yang sedang login"""
    try:
        user_id = request.headers.get("User-ID")
        if not user_id:
            return jsonify({"error": "User-ID header is required"}), 400

        user = get_user_by_id(int(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user.to_dict()), 200

    except Exception as e:
        logging.error(f"Error retrieving user profile: {str(e)}")
        return jsonify({"error": "Error retrieving user profile", "details": str(e)}), 500


@bp.route("/me", methods=["PUT"])
def update_profile():
    """Memperbarui profil user"""
    try:
        user_id = request.headers.get("User-ID")
        if not user_id:
            return jsonify({"error": "User-ID header is required"}), 400

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        username = data.get("username")
        password = data.get("password")

        # ✅ Hash password hanya jika ada password baru
        hashed_password = hash_password(password) if password else None

        # Ganti update_user_by_id dengan update_user_profile
        updated_user = update_user_profile(email=None, username=username, password=hashed_password, user_id=int(user_id))  # Sesuaikan argumen sesuai dengan perubahan fungsi
        if not updated_user:
            return jsonify({"error": "Failed to update user"}), 400

        return jsonify(updated_user.to_dict()), 200

    except Exception as e:
        logging.error(f"Error updating user profile: {str(e)}")
        return jsonify({"error": "Error updating user profile", "details": str(e)}), 500
