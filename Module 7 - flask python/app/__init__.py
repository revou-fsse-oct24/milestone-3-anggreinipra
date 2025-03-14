from flask import Flask
from flask_bcrypt import Bcrypt
from app.routes import bp  # Pastikan ini mengimpor Blueprint dengan benar

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Inisialisasi ekstensi Flask
    bcrypt.init_app(app)

    # Daftarkan Blueprint
    app.register_blueprint(bp)

    return app
