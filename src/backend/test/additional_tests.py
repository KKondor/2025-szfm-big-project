import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest

# Lightweight reporter to match existing tests' style
def report_result(description: str, expected: str, actual: str, match: bool):
    output = (
        f"\n🔹 {description}\n"
        f"   ➤ Elvárt eredmény: {expected}\n"
        f"   📥 Kapott eredmény: {actual}\n"
        f"   ✅ Egyezés: {match}\n"
    )
    print(output)
    with open("additional_tests_eredmenyek.log", "a", encoding="utf-8") as log_file:
        log_file.write(output)


def test_import_services_modules():
    description = "Import service modules"
    expected = "Modules import without ImportError"
    try:
        import services
        from services import users_service, foods_service, orders_service, auth_service, chatbot_service
        actual = "Imported"
        match = True
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_services_have_instances():
    description = "Service instances available"
    expected = "Instances exist: user_service, food_service, order_service, chatbot_service"
    try:
        from services import user_service, food_service, order_service, chatbot_service
        names = [hasattr(globals().get(n), '__class__') for n in ['user_service','food_service','order_service','chatbot_service']]
        actual = f"Instances: {', '.join([n for n in ['user_service','food_service','order_service','chatbot_service']])}"
        match = all([True for _ in names])
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_chatbot_service_interface():
    description = "Chatbot service exposes methods"
    expected = "has send_message and clear_history"
    try:
        from services import chatbot_service
        has_send = callable(getattr(chatbot_service, 'send_message', None))
        has_clear = callable(getattr(chatbot_service, 'clear_history', None))
        actual = f"send_message: {has_send}, clear_history: {has_clear}"
        match = has_send and has_clear
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_chatbot_conversation_history_structure():
    description = "Chatbot conversation_history is a dict"
    expected = "dict type"
    try:
        from services import chatbot_service
        actual = type(chatbot_service.conversation_history).__name__
        match = isinstance(chatbot_service.conversation_history, dict)
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_chatbot_clear_history_no_error():
    description = "Clear history no-op does not raise"
    expected = "no exception"
    try:
        from services import chatbot_service
        # ensure key not present
        chatbot_service.clear_history(999999)
        actual = "cleared/ignored"
        match = True
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_chatbot_set_and_clear_history():
    description = "Setting then clearing conversation history removes key"
    expected = "key removed"
    try:
        from services import chatbot_service
        chatbot_service.conversation_history[123456] = object()
        chatbot_service.clear_history(123456)
        actual = str(123456 in chatbot_service.conversation_history)
        match = 123456 not in chatbot_service.conversation_history
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_requirements_contains_generativeai():
    description = "requirements.txt lists google-generativeai"
    expected = "dependency present"
    try:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        req_path = os.path.join(base, 'requirements.txt')
        with open(req_path, 'r', encoding='utf-8') as f:
            content = f.read()
        actual = 'google-generativeai' in content
        match = actual
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, str(actual), match)
    assert match

def test_requirements_contains_flask():
    description = "requirements.txt lists Flask"
    expected = "dependency present"
    try:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        req_path = os.path.join(base, 'requirements.txt')
        with open(req_path, 'r', encoding='utf-8') as f:
            content = f.read()
        actual = 'Flask' in content
        match = actual
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, str(actual), match)
    assert match

def test_services_module_init_exports():
    description = "services package exports common symbols"
    expected = "exports user_service, food_service"
    try:
        import services
        has_user = hasattr(services, 'user_service')
        has_food = hasattr(services, 'food_service')
        actual = f"user_service: {has_user}, food_service: {has_food}"
        match = has_user and has_food
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_api_routes_module_contains_chatbot_endpoints():
    description = "api_routes defines chatbot endpoints"
    expected = "api_chatbot_message and api_clear_chatbot_history exist"
    try:
        from routes import api_routes
        has_msg = hasattr(api_routes, 'api_chatbot_message')
        has_clear = hasattr(api_routes, 'api_clear_chatbot_history')
        actual = f"msg: {has_msg}, clear: {has_clear}"
        match = has_msg and has_clear
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_food_service_methods_exist():
    description = "foods_service exposes CRUD methods"
    expected = "create_food, get_food, get_all_food, update_food, delete_food"
    try:
        from services import food_service
        methods = ['create_food','get_food','get_all_food','update_food','delete_food']
        missing = [m for m in methods if not hasattr(food_service, m)]
        actual = f"missing: {missing}"
        match = len(missing) == 0
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_user_service_methods_exist():
    description = "users_service exposes expected methods"
    expected = "get_all_users and change_user_role exist"
    try:
        from services import user_service
        has_get_all = hasattr(user_service, 'get_all_users')
        has_change = hasattr(user_service, 'change_user_role')
        actual = f"get_all: {has_get_all}, change_role: {has_change}"
        match = has_get_all and has_change
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_order_service_methods_exist():
    description = "orders_service exposes create_order and get_order_by_user_id"
    expected = "methods present"
    try:
        from services import order_service
        has_create = hasattr(order_service, 'create_order')
        has_get_user = hasattr(order_service, 'get_order_by_user_id')
        actual = f"create: {has_create}, get_by_user: {has_get_user}"
        match = has_create and has_get_user
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_auth_service_methods_exist():
    description = "auth_service exposes register and login"
    expected = "register and login exist"
    try:
        from services import auth_service
        has_reg = hasattr(auth_service, 'register')
        has_login = hasattr(auth_service, 'login')
        actual = f"register: {has_reg}, login: {has_login}"
        match = has_reg and has_login
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_repo_db_connect_exists():
    description = "db_connect.get_connection exists"
    expected = "function present"
    try:
        from repository.db_connect import get_connection
        actual = callable(get_connection)
        match = True if callable(get_connection) else False
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, str(actual), match)
    assert match

def test_repository_user_definitions():
    description = "User dataclass and Role exist in repository.users"
    expected = "User and Role present"
    try:
        from repository.users import User, Role
        actual = f"User: {User.__name__}, Role: {Role.__name__}"
        match = True
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_repository_order_status_exists():
    description = "OrderStatus enum exists"
    expected = "OrderStatus present"
    try:
        from repository.orders import OrderStatus
        actual = OrderStatus.__name__
        match = True
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_basic_flask_app_importable():
    description = "Flask app importable"
    expected = "app object is importable"
    try:
        from app import app
        actual = type(app).__name__
        match = True
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_static_images_directory_exists():
    description = "Static images directory exists"
    expected = "frontend/static/images directory present"
    try:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        images_dir = os.path.abspath(os.path.join(base, '..', 'frontend', 'static', 'images'))
        actual = os.path.isdir(images_dir)
        match = actual
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, str(actual), match)
    assert match

def test_env_file_contains_ai_key():
    description = "Backend .env contains AI_API_KEY"
    expected = "AI_API_KEY present in .env"
    try:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        env_path = os.path.join(base, '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                content = f.read()
            actual = 'AI_API_KEY' in content
            match = actual
        else:
            actual = 'no .env file'
            match = False
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, str(actual), match)
    assert match

def test_frontend_templates_exist():
    description = "Frontend templates directory exists"
    expected = "src/frontend/templates exists"
    try:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        templates_path = os.path.abspath(os.path.join(base, '..', 'frontend', 'templates'))
        actual = os.path.isdir(templates_path)
        match = actual
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, str(actual), match)
    assert match