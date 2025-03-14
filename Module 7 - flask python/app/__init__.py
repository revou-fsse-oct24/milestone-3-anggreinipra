from flask import Flask
from flask_bcrypt import Bcrypt
import logging

# ✅ Import Blueprint utama (yang sudah menggabungkan semua routes)
from app.routes import bp

# ✅ Inisialisasi Flask-Bcrypt
bcrypt = Bcrypt()

def create_app():
    """Fungsi untuk membuat instance Flask app"""
    app = Flask(__name__)

    # ✅ Tambahkan konfigurasi SECRET_KEY (penting untuk keamanan)
    app.config["SECRET_KEY"] = "supersecretkey"

    # ✅ Konfigurasi logging
    logging.basicConfig(level=logging.DEBUG)

    # ✅ Inisialisasi Flask-Bcrypt
    bcrypt.init_app(app)

    # ✅ Registrasi Blueprint utama
    app.register_blueprint(bp)

    return app
