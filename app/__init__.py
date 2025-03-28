from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

# Inisialisasi extension
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inisialisasi dengan aplikasi
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprint
    from app.routes import api_bp
    app.register_blueprint(api_bp)

    return app
