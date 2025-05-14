from flask import Blueprint, request, jsonify
from models.user import UserProfile, get_db
from utils.auth_middleware import token_required
from utils.permission_utils import require_permission, Permission

user_bp = Blueprint("user", __name__)

@user_bp.route('/user-profile', methods=['POST'])
def create_profile():
    data = request.get_json()
    db = get_db()
    
    if db.query(UserProfile).filter(UserProfile.user_id == data.get('user_id')).first():
        return jsonify({'message': 'Profile already exists'}), 409
    
    new_profile = UserProfile(
        user_id=data.get('user_id'),
        name=data.get('name'),
        email=data.get('email'),
        phone_number=data.get('phone_number'),
        role=data.get('role', 'user')
    )
    
    db.add(new_profile)
    db.commit()
    
    return jsonify({'message': 'Profile created successfully', 'user_id': new_profile.user_id}), 201

@user_bp.route('/users', methods=['GET'])
@token_required
@require_permission(Permission.MANAGE_USERS)
def get_all_users(current_user):
    db = get_db()
    users = db.query(UserProfile).all()
    
    return jsonify([
        {
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email,
            'phone_number': user.phone_number,
            'role': user.role
        }
        for user in users
    ]), 200

@user_bp.route('/users/<user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    if user_id != current_user.get('sub') and not Permission.has_permission(current_user.get('role'), Permission.MANAGE_USERS):
        return jsonify({'message': 'Permission denied'}), 403
    
    db = get_db()
    user = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'user_id': user.user_id,
        'name': user.name,
        'email': user.email,
        'phone_number': user.phone_number,
        'role': user.role
    }), 200