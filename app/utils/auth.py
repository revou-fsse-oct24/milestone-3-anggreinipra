import bcrypt
from flask import Request, request
from app.models import get_user_by_email

# ==============================
# ✅ PASSWORD HASHING
# ==============================

def hash_password(password: str) -> str:
    """Meng-hash password menggunakan bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    """Memeriksa apakah password cocok dengan hash yang tersimpan"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

# ==============================
# ✅ USER AUTHENTICATION
# ==============================

def authenticate_user(req: Request):  # 🔹 Ganti flask.request → flask.Request
    """
    Autentikasi user dari request menggunakan email di `Authorization: Bearer <email>`.
    Ini hanya simulasi karena tidak ada sistem token/JWT.
    """
    auth_header = req.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None  # Tidak ada header atau format salah

    email = auth_header.split("Bearer ")[1].strip()
    
    if not email:
        return None  # Email kosong

    user = get_user_by_email(email)
    return user if user else None
