"""
API routes for user authentication, food management, and orders.
"""
import os
from flask import Blueprint, request, jsonify, session, current_app as app
from werkzeug.utils import secure_filename
from services import users_service, foods_service, orders_service, auth_service, chatbot_service
from repository.users import User, Role
from repository.orders import OrderStatus

api_bp = Blueprint('api', __name__, url_prefix='/api')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

        result = auth_service.register(name, email, password, phone, address)
        
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

        result = auth_service.login(email, password)
        
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

        # Call service — let it raise errors
        auth_service.change_password(email, new_password)

        # If no exception was thrown → success
        return jsonify({'success': True, 'message': "Password change succesful."}), 200

    except ValueError as e:
        # User error (bad input or missing user)
        return jsonify({'success': False, 'message': str(e)}), 400

    except RuntimeError as e:
        # DB/update error
        return jsonify({'success': False, 'message': str(e)}), 500

    except Exception as e:
        # Unhandled unexpected error
        return jsonify({'success': False, 'message': f"Server error: {str(e)}"}), 500

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

@api_bp.route('/foods/files', methods=['POST'])
def api_create_food_files():
    try:
        if session.get('user_role') != 'admin':
            return jsonify({'success': False, 'message': 'Admin access required'}), 403

        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category = request.form.get('category')

        price = float(price) if price else None

        file = request.files.get('image')
        image_filename = None
        if file and allowed_file(file.filename):
            image_filename = secure_filename(file.filename)
            save_path = os.path.join(app.static_folder, 'images', image_filename)
            file.save(save_path)

        foods_service.create_food(name, description, image_filename, price, category)
        return jsonify({'success': True, 'message': 'Food created successfully'}), 201

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
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
    
@api_bp.route('/foods/files/<int:food_id>', methods=['PUT'])
def api_update_food_files(food_id):
    try:
        if session.get('user_role') != 'admin':
            return jsonify({'success': False, 'message': 'Admin access required'}), 403
        # Get text fields
        name = request.form.get('name')
        description = request.form.get('description')
        price = int(request.form.get('price'))
        category = request.form.get('category')

        # Get file
        file = request.files.get('food-image') 
        image_filename = request.form.get('old-image') 
        if file and allowed_file(file.filename):
            image_filename = secure_filename(file.filename)
            save_path = os.path.join(app.static_folder, 'images', image_filename)
            file.save(save_path)

        foods_service.update_food(food_id, name, description, image_filename, price, category)
        return jsonify({'success': True, 'message': 'Food updated successfully'}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

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


# ==================== ORDER ENDPOINTS ====================

@api_bp.route('/orders', methods=['POST'])
def api_create_order():
    """Create a new order."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': 'User must be logged in'}), 401

        data = request.get_json()
        food_ids = data.get('food_ids', [])
        note = data.get('note', '')

        if not isinstance(food_ids, list) or len(food_ids) == 0:
            return jsonify({'success': False, 'message': 'food_ids must be a non-empty list'}), 400

        orders_service.create_order(user_id, food_ids, note)
        return jsonify({'success': True, 'message': 'Order created successfully'}), 201
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500


@api_bp.route('/orders', methods=['GET'])
def api_get_all_orders():
    """Get all orders. (Admin only)"""
    try:
        if session.get('user_role') != 'admin':
            return jsonify({'success': False, 'message': 'Admin access required'}), 403

        orders = orders_service.get_all_orders()
        return jsonify({
            'success': True,
            'orders': [
                {
                    'order_id': order.order_id,
                    'user_id': order.user.id,
                    'user_name': order.user.name,
                    'order_date': order.order_date.isoformat() if order.order_date else None,
                    'status': order.status.value,
                    'note': order.note,
                    'total_price': order.total_price,
                    'items': [
                        {
                            'item_id': item.item_id,
                            'food_id': item.food.id,
                            'food_name': item.food.name,
                            'quantity': item.quantity,
                            'item_price': item.item_price
                        }
                        for item in order.items
                    ]
                }
                for order in orders
            ]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500


@api_bp.route('/orders/user/<int:user_id>', methods=['GET'])
def api_get_user_orders(user_id):
    """Get all orders for a specific user. User can only see their own orders unless admin."""
    try:
        current_user_id = session.get('user_id')
        is_admin = session.get('user_role') == 'admin'

        if not is_admin and current_user_id != user_id:
            return jsonify({'success': False, 'message': 'Access denied'}), 403

        orders = orders_service.get_order_by_user_id(user_id)
        return jsonify({
            'success': True,
            'orders': [
                {
                    'order_id': order.order_id,
                    'user_id': order.user.id,
                    'order_date': order.order_date.isoformat() if order.order_date else None,
                    'status': order.status.value,
                    'note': order.note,
                    'total_price': order.total_price,
                    'items': [
                        {
                            'item_id': item.item_id,
                            'food_id': item.food.id,
                            'food_name': item.food.name,
                            'quantity': item.quantity,
                            'item_price': item.item_price
                        }
                        for item in order.items
                    ]
                }
                for order in orders
            ]
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500


@api_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def api_update_order_status(order_id):
    """Update order status. (Admin only)"""
    try:
        if session.get('user_role') != 'admin':
            return jsonify({'success': False, 'message': 'Admin access required'}), 403

        data = request.get_json()
        new_status = data.get('status')

        if new_status not in ['pending', 'completed', 'cancelled']:
            return jsonify({'success': False, 'message': 'Status must be "pending", "completed", or "cancelled"'}), 400

        from repository.orders import OrderStatus
        orders_service.update_order_status(order_id, OrderStatus(new_status))
        return jsonify({'success': True, 'message': 'Order status updated successfully'}), 200
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500



# ==================== USER MANAGEMENT ENDPOINTS ====================

@api_bp.route('/users', methods=['GET'])
def api_get_all_users():
    """Get all users. (Admin only)"""
    try:
        if session.get('user_role') != 'admin':
            return jsonify({'success': False, 'message': 'Admin access required'}), 403

        result = users_service.get_all_users()
        
        if isinstance(result, list):
            return jsonify({
                'success': True,
                'users': [
                    {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'phone': user.phone,
                        'address': user.address,
                        'role': user.role.value
                    }
                    for user in result
                ]
            }), 200
        else:
            return jsonify({'success': False, 'message': result}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500


@api_bp.route('/users/<email>', methods=['GET'])
def api_get_user(email):
    """Get user by email."""
    try:
        user = auth_service.get_user_by_email(email)
        
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


@api_bp.route('/users/<int:user_id>/role', methods=['PUT'])
def api_change_user_role(user_id):
    """Change a user's role. (Admin only)"""
    try:
        if session.get('user_role') != 'admin':
            return jsonify({'success': False, 'message': 'Admin access required'}), 403

        data = request.get_json()
        new_role_value = data.get('role')

        if new_role_value not in ['user', 'admin']:
            return jsonify({'success': False, 'message': 'Role must be "user" or "admin"'}), 400

        from backend.repository.users import Role
        new_role = Role(new_role_value)
        result = users_service.change_user_role(user_id, new_role)

        if result == "A jogosultság sikeresen módosítva.":
            return jsonify({'success': True, 'message': result}), 200
        else:
            return jsonify({'success': False, 'message': result}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500


@api_bp.route('/chatbot/clear-history', methods=['POST'])
def api_clear_chatbot_history():
    """Clear chatbot conversation history for the current user."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': 'User must be logged in'}), 401

        chatbot_service.clear_history(user_id)
        return jsonify({
            'success': True,
            'message': 'Conversation history cleared'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500


@api_bp.route('/chatbot/message', methods=['POST'])
def api_chatbot_message():
    """Send a message to the AI chatbot and return its reply."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': 'User must be logged in'}), 401

        data = request.get_json(silent=True) or {}
        message = data.get('message') or data.get('text')
        if not message:
            return jsonify({'success': False, 'message': 'No message provided'}), 400

        reply = chatbot_service.send_message(user_id, message)
        return jsonify({'success': True, 'reply': reply}), 200
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500
