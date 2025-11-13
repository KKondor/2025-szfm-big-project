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

# ==================== FOOD MANAGEMENT ENDPOINTS ====================

@api_bp.route('/foods', methods=['GET'])
def api_get_all_foods():
    """Get all foods."""
    try:
        foods = foods_service.get_all_food()
        return jsonify({
            'success': True,
            'foods': [
                {
                    'id': food.id,
                    'name': food.name,
                    'description': food.description,
                    'image': food.image,
                    'price': food.price,
                    'category': food.category
                }
                for food in foods
            ]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500
    
@api_bp.route('/foods/<int:food_id>', methods=['GET'])
def api_get_food(food_id):
    """Get food by ID."""
    try:
        food = foods_service.get_food(food_id)
        
        if food:
            return jsonify({
                'success': True,
                'food': {
                    'id': food.id,
                    'name': food.name,
                    'description': food.description,
                    'image': food.image,
                    'price': food.price,
                    'category': food.category
                }
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Food not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500
    
@api_bp.route('/foods', methods=['POST'])
def api_create_food():
    """Create a new food item. (Admin only)"""
    try:
        # Check if user is admin
        if session.get('user_role') != 'admin':
            return jsonify({'success': False, 'message': 'Admin access required'}), 403

        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        image = data.get('image')
        price = data.get('price')
        category = data.get('category')

        if not all([name, price]):
            return jsonify({'success': False, 'message': 'Name and price are required'}), 400

        foods_service.create_food(name, description, image, price, category)
        return jsonify({'success': True, 'message': 'Food created successfully'}), 201
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500
    
@api_bp.route('/foods/<int:food_id>', methods=['PUT'])
def api_update_food(food_id):
    """Update a food item. (Admin only)"""
    try:
        if session.get('user_role') != 'admin':
            return jsonify({'success': False, 'message': 'Admin access required'}), 403

        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        image = data.get('image')
        price = data.get('price')
        category = data.get('category')

        if not all([name, price]):
            return jsonify({'success': False, 'message': 'Name and price are required'}), 400

        foods_service.update_food(food_id, name, description, image, price, category)
        return jsonify({'success': True, 'message': 'Food updated successfully'}), 200
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500
    
@api_bp.route('/foods/<int:food_id>', methods=['DELETE'])
def api_delete_food(food_id):
    """Delete a food item. (Admin only)"""
    try:
        if session.get('user_role') != 'admin':
            return jsonify({'success': False, 'message': 'Admin access required'}), 403

        foods_service.delete_food(food_id)
        return jsonify({'success': True, 'message': 'Food deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500
