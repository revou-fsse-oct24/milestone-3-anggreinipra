from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes import bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    jwt = JWTManager(app)
    return app