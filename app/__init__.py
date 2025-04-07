from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from dotenv import load_dotenv

# Load environment variables dari .env
load_dotenv()

# Inisialisasi extension
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inisialisasi extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.users import users_bp
    from app.routes.accounts import accounts_bp
    from app.routes.transactions import transactions_bp

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(accounts_bp, url_prefix="/accounts")
    app.register_blueprint(transactions_bp, url_prefix="/transactions")

    return app
