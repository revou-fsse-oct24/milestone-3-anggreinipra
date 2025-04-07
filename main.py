from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.database import db
from app.routes import register_blueprints
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    # Register Blueprints
    register_blueprints(app)

    @app.route('/')
    def index():
        return {'message': 'Welcome to RevoBank API 🔐'}, 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
