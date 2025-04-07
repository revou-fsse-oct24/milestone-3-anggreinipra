from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.accounts import Account
from app.models.users import User
from app.database import db

accounts_bp = Blueprint('accounts', __name__, url_prefix="/accounts")

# GET /accounts → Retrieve all accounts
@accounts_bp.route('', methods=['GET'])  # /accounts
def get_all_accounts():
    # Optional: support email filter ?email=
    email = request.args.get('email')
    if email:
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        accounts = Account.query.filter_by(user_id=user.user_id).all()
        return jsonify([acc.to_dict() for acc in accounts]), 200

    accounts = Account.query.all()
    return jsonify([account.to_dict() for account in accounts]), 200


# GET /accounts/<account_number> → Retrieve account by account_number
@accounts_bp.route('/<string:account_number>', methods=['GET'])  # /accounts/<account_number>
@jwt_required()
def get_account_by_number(account_number):
    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify(account.to_dict()), 200


# PUT /accounts/<account_number> → Update account
@accounts_bp.route('/<string:account_number>', methods=['PUT'])  # /accounts/<account_number>
@jwt_required()
def update_account(account_number):
    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return jsonify({'error': 'Account not found'}), 404

    data = request.get_json()
    if 'account_type' in data:
        account.account_type = data['account_type']
    db.session.commit()

    return jsonify({'message': 'Account updated successfully'}), 200


# DELETE /accounts/<account_number> → Delete account if balance == 0
@accounts_bp.route('/<string:account_number>', methods=['DELETE'])  # /accounts/<account_number>
@jwt_required()
def delete_account(account_number):
    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return jsonify({'error': 'Account not found'}), 404

    if account.balance > 0:
        return jsonify({'error': 'Account cannot be deleted unless balance is 0'}), 400

    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': 'Account deleted successfully'}), 200
