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
