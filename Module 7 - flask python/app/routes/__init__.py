from flask import Blueprint, render_template, jsonify, request
from app.models import get_all_users, get_user_by_id, add_user, delete_user, update_user_by_email

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/users', methods=['GET'])
def users():
    all_users = get_all_users()
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "account_number": user.account_number
    } for user in all_users])

@bp.route('/users/<int:user_id>', methods=['GET'])
def user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "account_number": user.account_number
        })
    return jsonify({"message": "User not found, please register first"}), 404

@bp.route('/users', methods=['POST'])
def add_new_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    new_user = add_user(username, email, password)  
    return jsonify({
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "account_number": new_user.account_number
    }), 201
    
@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    user = get_user_by_id(user_id)
    if user:
        delete_user(user_id)
        return jsonify({"message": "User successfully deleted"}), 200
    return jsonify({"message": "User not found"}), 404

@bp.route('/users/<string:email>', methods=['PUT'])
def update_user(email):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    updated_user = update_user_by_email(email, username, password)
    if updated_user:
        return jsonify({
            "id": updated_user.id,
            "username": updated_user.username,
            "email": updated_user.email,
            "account_number": updated_user.account_number
        })
    return jsonify({"message": "User not found, please register first"}), 404