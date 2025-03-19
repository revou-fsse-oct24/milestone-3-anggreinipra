from flask import Blueprint

# 🔹 Blueprint utama API
api_bp = Blueprint('api', __name__)

# 🔹 Import dan daftarkan submodule dengan Blueprint mereka sendiri
from app.routes.accounts import accounts_bp
from app.routes.users import users_bp
from app.routes.transactions import transactions_bp

api_bp.register_blueprint(accounts_bp, url_prefix='/accounts')
api_bp.register_blueprint(users_bp, url_prefix='/users')
api_bp.register_blueprint(transactions_bp, url_prefix='/transactions')
