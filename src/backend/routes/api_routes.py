"""
API routes for user authentication, food management, and orders.
"""
from flask import Blueprint, request, jsonify, session
from backend.services import users_service, foods_service, orders_service
from backend.repository.users import User

api_bp = Blueprint('api', __name__, url_prefix='/api')

# ==================== USER AUTHENTICATION ENDPOINTS ====================

@api_bp.route('/auth/register', methods=['POST'])
def api_register():
    """Register a new user."""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone', '')
        address = data.get('address', '')

        if not all([name, email, password]):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400

        result = users_service.register(name, email, password, phone, address)
        
        if result == "Regisztráció sikeres.":
            return jsonify({'success': True, 'message': result}), 201
        else:
            return jsonify({'success': False, 'message': result}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500
    
@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    """User login endpoint."""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400

        result = users_service.login(email, password)
        
        if isinstance(result, User):
            session['user_id'] = result.id
            session['user_role'] = result.role.value
            return jsonify({
                'success': True, 
                'message': 'Bejelentkezés sikeres.',
                'user': {
                    'id': result.id,
                    'name': result.name,
                    'email': result.email,
                    'role': result.role.value
                }
            }), 200
        else:
            return jsonify({'success': False, 'message': result}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500
    
@api_bp.route('/auth/logout', methods=['POST'])
def api_logout():
    """User logout endpoint."""
    try:
        session.clear()
        return jsonify({'success': True, 'message': 'Kijelentkezés sikeres.'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500
    
@api_bp.route('/auth/change-password', methods=['POST'])
def api_change_password():
    """Change user password."""
    try:
        data = request.get_json()
        email = data.get('email')
        new_password = data.get('new_password')

        if not email or not new_password:
            return jsonify({'success': False, 'message': 'Email and new password required'}), 400

        result = users_service.change_password(email, new_password)
        
        if result == "A jelszó sikeresen megváltozott.":
            return jsonify({'success': True, 'message': result}), 200
        else:
            return jsonify({'success': False, 'message': result}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500
    
@api_bp.route('/auth/get-user/<email>', methods=['GET'])
def api_get_user(email):
    """Get user by email."""
    try:
        user = users_service.get_user_by_email(email)
        
        if user:
            return jsonify({
                'success': True,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'phone': user.phone,
                    'address': user.address,
                    'role': user.role.value
                }
            }), 200
        else:
            return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500
