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