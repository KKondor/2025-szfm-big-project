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