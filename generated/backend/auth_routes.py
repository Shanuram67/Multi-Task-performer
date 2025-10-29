from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    # TODO: lookup user in DB, verify password
    return jsonify({ 'message':'login-ok', 'token': None })