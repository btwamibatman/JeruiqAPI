from flask import Blueprint, request, jsonify
from models.user import UserProfile, get_db
from utils.auth_middleware import token_required
from utils.permission_utils import require_permission, Permission

role_bp = Blueprint("role", __name__)

@role_bp.route('/users/<user_id>/role', methods=['PUT'])
@token_required
@require_permission(Permission.MANAGE_USERS)
def update_role(current_user, user_id):
    data = request.get_json()
    new_role = data.get('role')
    
    if not new_role:
        return jsonify({'message': 'Role is required'}), 400
    
    db = get_db()
    user = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user.role = new_role
    db.commit()
    
    return jsonify({'message': 'Role updated successfully', 'user_id': user.user_id, 'role': user.role}), 200