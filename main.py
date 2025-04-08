from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.database import db
from app.routes import register_blueprints
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Flask configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    # Register blueprints for routes
    register_blueprints(app)

    # Optional welcome route
    @app.route('/')
    def index():
        return {'message': 'Welcome to RevoBank API 🔐'}, 200

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
