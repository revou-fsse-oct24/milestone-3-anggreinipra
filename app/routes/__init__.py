from flask import Blueprint
from .users import users_bp
from .accounts import accounts_bp
from .transactions import transactions_bp

def register_blueprints(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(transactions_bp)

