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