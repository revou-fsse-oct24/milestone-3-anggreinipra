import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_secret_key')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', True)

    # PostgreSQL settings from individual components (for flexibility/debugging)
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    DB_HOST = os.getenv('POSTGRES_HOST', 'db')
    DB_PORT = os.getenv('POSTGRES_PORT', 5432)
    DB_NAME = os.getenv('POSTGRES_DB', 'revobank')

    # Full SQLAlchemy database URI (used by Flask & Alembic)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # SQLAlchemy behavior
    SQLALCHEMY_TRACK_MODIFICATIONS = False
