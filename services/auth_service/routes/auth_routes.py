from flask import Blueprint, request, jsonify
from models.user import User, get_db
from utils.hash_utils import hash_password, verify_password
from utils.token_utils import generate_token, decode_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    email, password = data.get('email'), data.get('password')
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400
    
    db = get_db()
    
    if db.query(User).filter(User.email == email).first():
        return jsonify({'message': 'User already exists'}), 409
    
    new_user = User(email=email, password_hash=hash_password(password))
    db.add(new_user)
    db.commit()
    
    return jsonify({'message': 'User created successfully', 'user_id': new_user.user_id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email, password = data.get('email'), data.get('password')
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400
    
    db = get_db()
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.password_hash):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = generate_token(user.user_id, user.email, user.role)
    return jsonify({'token': token, 'user_id': user.user_id, 'email': user.email, 'role': user.role}), 200

@auth_bp.route('/auth/validate-token', methods=['POST'])
def validate_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Invalid authorization header'}), 401
    
    token = auth_header.split(' ')[1]
    decoded = decode_token(token)
    
    if 'message' in decoded:
        return jsonify({'message': decoded['message']}), 401
    
    return jsonify(decoded), 200