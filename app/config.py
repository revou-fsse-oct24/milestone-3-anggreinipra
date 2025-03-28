import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', True)

    # Database settings (menggunakan variabel terpisah)
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'your_password')
    DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', 5432)
    DB_NAME = os.getenv('POSTGRES_DB', 'revobank')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/revobank')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
