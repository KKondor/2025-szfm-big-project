import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from services.orders_service import order_service
from repository.orders import OrderStatus
from repository.orders import Order
from repository.foods import Food
from repository.users import User
from repository.db_connect import get_connection

# Tesztadatok
VALID_USER_ID = 4
VALID_FOOD_IDS = [1, 2]
INVALID_USER_ID = 999
INVALID_FOOD_IDS = [999]
TOO_LONG_NOTE = "x" * 501

# 🔧 Tesztlogika
def report_result(description: str, expected: str, actual: str, match: bool):
    output = (
        f"\n🔹 {description}\n"
        f"   ➤ Elvárt eredmény: {expected}\n"
        f"   📥 Kapott eredmény: {actual}\n"
        f"   ✅ Egyezés: {match}\n"
    )
    print(output)
    with open("orders_teszt_eredmenyek.log", "a", encoding="utf-8") as log_file:
        log_file.write(output)

'''
# -------------------------
# SIKERES RENDELÉS LÉTREHOZÁSA
# -------------------------
'''

def test_create_order_success_and_cleanup():
    description = "Sikeres rendelés létrehozása és törlése"
    expected = "Rendelés bekerült, majd törölve lett"

    created_order_id = None
    test_note = "Teszt rendelés törléshez"

    try:
        order_service.create_order(VALID_USER_ID, VALID_FOOD_IDS, test_note)

        orders = order_service.get_order_by_user_id(VALID_USER_ID)
        matching_orders = [o for o in orders if o.note == test_note]
        match = len(matching_orders) > 0
        actual = f"Talált rendelés: {matching_orders[0].order_id}" if match else "Nem található"

        if match:
            created_order_id = matching_orders[0].order_id

    except Exception as e:
        actual = str(e)
        match = False

    finally:
        if created_order_id:
            try:
                from repository.db_connect import get_connection
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM order_items WHERE order_id = %s", (created_order_id,))
                cursor.execute("DELETE FROM orders WHERE id = %s", (created_order_id,))
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as cleanup_error:
                print(f"Hiba a törlés során: {cleanup_error}")

    report_result(description, expected, actual, match)
    assert match

'''
# -------------------------
# HIBÁS RENDELÉS LÉTREHOZÁSA
# -------------------------
'''

def test_create_order_invalid_user():
    description = "Rendelés nem létező user ID-val"
    expected = "Hiba: User with ID 999 does not exist"

    try:
        order_service.create_order(INVALID_USER_ID, VALID_FOOD_IDS, "Teszt")
        actual = "Sikerült létrehozni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "does not exist" in actual

    report_result(description, expected, actual, match)
    assert match

def test_create_order_invalid_food():
    description = "Rendelés nem létező étel ID-val"
    expected = "Hiba: Food with ID 999 does not exist"

    try:
        order_service.create_order(VALID_USER_ID, INVALID_FOOD_IDS, "Teszt")
        actual = "Sikerült létrehozni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "does not exist" in actual

    report_result(description, expected, actual, match)
    assert match

def test_create_order_empty_food_list():
    description = "Rendelés üres étel listával"
    expected = "Hiba: food_ids must be a non-empty list of food IDs"

    try:
        order_service.create_order(VALID_USER_ID, [], "Teszt")
        actual = "Sikerült létrehozni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "non-empty list" in actual

    report_result(description, expected, actual, match)
    assert match

def test_create_order_note_too_long():
    description = "Rendelés túl hosszú megjegyzéssel"
    expected = "Hiba: Note must be 500 characters or fewer"

    try:
        order_service.create_order(VALID_USER_ID, VALID_FOOD_IDS, TOO_LONG_NOTE)
        actual = "Sikerült létrehozni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "500 characters or fewer" in actual

    report_result(description, expected, actual, match)
    assert match

'''
# -------------------------
# STÁTUSZ MÓDOSÍTO TESZT
# -------------------------
'''

def test_update_order_status_and_cleanup():
    description = "Rendelés státusz módosítása és törlése"
    expected = "Státusz módosítva COMPLETED-re, majd rendelés törölve"

    created_order_id = None
    test_note = "Teszt státusz módosítás"

    try:
        order_service.create_order(VALID_USER_ID, VALID_FOOD_IDS, test_note)

        orders = order_service.get_order_by_user_id(VALID_USER_ID)
        matching_orders = [o for o in orders if o.note == test_note]
        match = len(matching_orders) > 0
        actual = f"Talált rendelés: {matching_orders[0].order_id}" if match else "Nem található"

        if match:
            created_order_id = matching_orders[0].order_id

            order_service.update_order_status(created_order_id, OrderStatus.COMPLETED)

            updated_order = [o for o in order_service.get_order_by_user_id(VALID_USER_ID) if o.order_id == created_order_id][0]
            match = updated_order.status == OrderStatus.COMPLETED
            actual = f"Új státusz: {updated_order.status}"

    except Exception as e:
        actual = str(e)
        match = False

    finally:
        if created_order_id:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM order_items WHERE order_id = %s", (created_order_id,))
                cursor.execute("DELETE FROM orders WHERE id = %s", (created_order_id,))
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as cleanup_error:
                print(f"Hiba a törlés során: {cleanup_error}")

    report_result(description, expected, actual, match)
    assert match


def test_update_order_status_invalid_id():
    description = "Státusz módosítása érvénytelen order_id értékkel"
    expected = "Hiba: order_id must be a positive integer"

    try:
        order_service.update_order_status(-5, OrderStatus.CANCELLED)
        actual = "Sikerült módosítani"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "positive integer" in actual

    report_result(description, expected, actual, match)
    assert match
