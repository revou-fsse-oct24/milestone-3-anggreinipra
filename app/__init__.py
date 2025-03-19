import logging
from flask import Flask, jsonify, request
from app.routes import api_bp  # Gunakan nama baru

def create_app():
    """Membuat dan mengonfigurasi aplikasi Flask"""
    app = Flask(__name__)

    # ✅ Register blueprint utama
    app.register_blueprint(api_bp)

    # ✅ Konfigurasi logging
    logging.basicConfig(level=logging.DEBUG)

    # ✅ Middleware untuk validasi JSON
    @app.before_request
    def validate_json():
        if request.method in ["POST", "PUT"] and not request.is_json:
            return jsonify({"message": "Request must be in JSON format"}), 400

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to RevoBank API!"})

    return app
