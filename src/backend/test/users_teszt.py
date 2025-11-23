import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import mysql.connector
import os
from services import auth_service
from services.users_service import user_service
from repository.users import Role
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Tesztadatok
VALID_NAME = "Test User"
VALID_EMAIL = "testuser@example.com"
VALID_PASSWORD = "StrongPass123"
VALID_PHONE = "123456789"
VALID_ADDRESS = "123 Test Street"

# 🔧 Adatbázis törlés közvetlenül
def delete_test_user(email: str):
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE email = %s", (email,))
    conn.commit()
    cursor.close()
    conn.close()

@pytest.fixture(scope="module", autouse=True)
def cleanup_user():
    delete_test_user(VALID_EMAIL)
    yield
    delete_test_user(VALID_EMAIL)

def report_result(description: str, expected: str, actual: str, match: bool):
    output = (
        f"\n🔹 {description}\n"
        f"   ➤ Elvárt eredmény: {expected}\n"
        f"   📥 Kapott eredmény: {actual}\n"
        f"   ✅ Egyezés: {match}\n"
    )
    print(output)
    with open("users_teszt_eredmenyek.log", "a", encoding="utf-8") as log_file:
        log_file.write(output)

'''
# -------------------------
# REGISZTRÁCIÓ TESZTEK
# -------------------------
'''

def test_register_success():
    description = "Sikeres regisztráció"
    expected = "Felhasználó létrejött és lekérdezhető"
    try:
        auth_service.register(VALID_NAME, VALID_EMAIL, VALID_PASSWORD, VALID_PHONE, VALID_ADDRESS)
        user = auth_service.get_user_by_email(VALID_EMAIL)
        actual = f"{user.name}, {user.email}" if user else "None"
        match = user is not None and user.email == VALID_EMAIL
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_register_duplicate_email():
    description = "Duplikált email regisztráció"
    expected = "Hiba: Email already exists"
    try:
        auth_service.register("Another", VALID_EMAIL, "AnotherPass123")
        actual = "Sikerült regisztrálni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "Email already exists" in actual
    report_result(description, expected, actual, match)
    assert match

def test_register_invalid_email():
    description = "Érvénytelen email formátum"
    expected = "Hiba: Invalid email format"
    try:
        auth_service.register("Invalid", "not-an-email", VALID_PASSWORD)
        actual = "Sikerült regisztrálni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "Invalid email format" in actual
    report_result(description, expected, actual, match)
    assert match

def test_register_weak_password():
    description = "Gyenge jelszó"
    expected = "Hiba: Password is not strong enough"
    try:
        auth_service.register("Weak", "weak@example.com", "123")
        actual = "Sikerült regisztrálni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "Password is not strong enough" in actual
    report_result(description, expected, actual, match)
    assert match

'''
# -------------------------
# BEJELENTKEZÉS TESZTEK
# -------------------------
'''

def test_login_success():
    description = "Sikeres bejelentkezés"
    expected = "Felhasználó visszatér"
    try:
        user = auth_service.login(VALID_EMAIL, VALID_PASSWORD)
        actual = f"{user.name}, {user.email}" if user else "None"
        match = user is not None and user.email == VALID_EMAIL
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_login_wrong_password():
    description = "Hibás jelszóval bejelentkezés"
    expected = "Hiba: Invalid email/username or password"
    try:
        auth_service.login(VALID_EMAIL, "WrongPassword123")
        actual = "Sikerült bejelentkezni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "Invalid email/username or password" in actual
    report_result(description, expected, actual, match)
    assert match

def test_login_nonexistent_user():
    description = "Nem létező felhasználóval bejelentkezés"
    expected = "Hiba: Invalid email/username or password"
    try:
        auth_service.login("ghost@example.com", "AnyPassword")
        actual = "Sikerült bejelentkezni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "Invalid email/username or password" in actual
    report_result(description, expected, actual, match)
    assert match
'''
# -------------------------
# JOGOSULTSÁG TESZT
# -------------------------
'''

def test_change_user_role():
    description = "Jogosultság módosítása USER → ADMIN → USER"
    expected = "ADMIN szerepkör beállítva, majd visszaállítva USER-re"
    try:
        user = auth_service.get_user_by_email(VALID_EMAIL)
        user_service.change_user_role(user.id, Role.ADMIN)
        updated = auth_service.get_user_by_email(VALID_EMAIL)
        user_service.change_user_role(user.id, Role.USER)
        reverted = auth_service.get_user_by_email(VALID_EMAIL)
        actual = f"ADMIN: {updated.role}, USER: {reverted.role}"
        match = updated.role == Role.ADMIN and reverted.role == Role.USER
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

'''
# -------------------------
# JELSZÓMÓDOSÍTÁS TESZTEK
# -------------------------
'''

def test_change_password_success():
    description = "Sikeres jelszómódosítás"
    expected = "Új jelszó beállítva, bejelentkezés sikeres"
    new_password = "NewStrongPass456"
    try:
        auth_service.change_password(VALID_EMAIL, new_password)
        user = auth_service.login(VALID_EMAIL, new_password)
        actual = f"{user.name}, {user.email}" if user else "None"
        match = user is not None and user.email == VALID_EMAIL
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_change_password_weak():
    description = "Gyenge új jelszó"
    expected = "Hiba: New password is not strong enough"
    weak_password = "123"
    try:
        auth_service.change_password(VALID_EMAIL, weak_password)
        actual = "Jelszó sikeresen módosítva"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "New password is not strong enough" in actual
    report_result(description, expected, actual, match)
    assert match

def test_change_password_nonexistent_email():
    description = "Nem létező emailre jelszómódosítás"
    expected = "Hiba: Email does not exist"
    try:
        auth_service.change_password("ghost@example.com", "ValidPass789")
        actual = "Jelszó sikeresen módosítva"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "Email does not exist" in actual
    report_result(description, expected, actual, match)
    assert match

'''
# -------------------------
# LEKÉRDEZÉS TESZTEK
# -------------------------
'''

def test_get_user_by_email_success():
    description = "Felhasználó lekérdezése email alapján"
    expected = "Felhasználó visszatér"
    try:
        user = auth_service.get_user_by_email(VALID_EMAIL)
        actual = f"{user.name}, {user.email}" if user else "None"
        match = user is not None and user.email == VALID_EMAIL
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

def test_get_all_users_contains_test_user():
    description = "Összes felhasználó lekérdezése"
    expected = "Tesztfelhasználó szerepel a listában"
    try:
        users = user_service.get_all_users()
        emails = [u.email for u in users]
        actual = f"Felhasználók: {emails}"
        match = VALID_EMAIL in emails
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

'''
# -------------------------
# ADMIN HOZZÁFÉRÉS TESZTEK
# -------------------------
'''

def test_admin_required_route_with_user_role(client):
    description = "Nem-admin felhasználó hozzáférése admin route-hoz"
    expected = "Hiba: hozzáférés megtagadva (403 vagy redirect)"

    with client.session_transaction() as sess:
        sess["user_role"] = "user"

    try:
        response = client.get("/admin")
        actual = f"Status code: {response.status_code}"
        match = response.status_code in [302, 403]
    except Exception as e:
        actual = str(e)
        match = False

    report_result(description, expected, actual, match)
    assert match

def test_admin_required_route_with_admin_role(client):
    description = "Admin felhasználó hozzáférése admin route-hoz"
    expected = "Sikeres hozzáférés (200)"

    with client.session_transaction() as sess:
        sess["user_id"] = 2
        sess["user_role"] = "admin"

    try:
        response = client.get("/admin")
        actual = f"Status code: {response.status_code}"
        match = response.status_code == 200
    except Exception as e:
        actual = str(e)
        match = False

    report_result(description, expected, actual, match)
    assert match

'''
# -------------------------
# INPUT VALIDÁCIÓS TESZTEK
# -------------------------
'''

def test_register_empty_fields():
    description = "Regisztráció üres mezőkkel"
    expected = "Hiba: Hiányzó kötelező mezők"
    try:
        auth_service.register("", "", "", "", "")
        actual = "Sikerült regisztrálni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "missing" in actual.lower() or "required" in actual.lower()
    report_result(description, expected, actual, match)
    assert match

def test_register_excessively_long_fields():
    description = "Regisztráció túl hosszú mezőkkel"
    expected = "Hiba: Name is required and must be 100 characters or fewer"
    long_name = "A" * 300
    long_email = ("a" * 250) + "@example.com"
    try:
        auth_service.register(long_name, long_email, VALID_PASSWORD, VALID_PHONE, VALID_ADDRESS)
        actual = "Sikerült regisztrálni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "name" in actual.lower() and "100" in actual
    report_result(description, expected, actual, match)
    assert match

def test_change_password_empty_input():
    description = "Jelszómódosítás üres jelszóval"
    expected = "New password is not strong enough"
    try:
        auth_service.change_password(VALID_EMAIL, "")
        actual = "Jelszó sikeresen módosítva"
        match = False
    except ValueError as e:
        actual = str(e)
        match = expected in actual
    report_result(description, expected, actual, match)
    assert match

def test_register_invalid_types():
    description = "Regisztráció nem szöveges típusokkal"
    expected = "Hiba: Típusellenőrzés nem ment át"
    try:
        auth_service.register(123, True, None, [], {})
        actual = "Sikerült regisztrálni"
        match = False
    except (ValueError, TypeError) as e:
        actual = str(e)
        match = "type" in actual.lower() or "invalid" in actual.lower()
    report_result(description, expected, actual, match)
    assert match

