import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from services.foods_service import food_service
from repository.foods import Food, FoodManager


# Tesztadatok
VALID_NAME = "Teszt Étel"
VALID_DESCRIPTION = "Finom és friss"
VALID_IMAGE = "image.jpg"
VALID_PRICE = 1200
VALID_CATEGORY = "Főétel"

# 🔧 Tesztlogika
def report_result(description: str, expected: str, actual: str, match: bool):
    output = (
        f"\n🔹 {description}\n"
        f"   ➤ Elvárt eredmény: {expected}\n"
        f"   📥 Kapott eredmény: {actual}\n"
        f"   ✅ Egyezés: {match}\n"
    )
    print(output)
    with open("foods_teszt_eredmenyek.log", "a", encoding="utf-8") as log_file:
        log_file.write(output)


@pytest.fixture
def test_food():
    food_service.create_food(VALID_NAME, VALID_DESCRIPTION, VALID_IMAGE, VALID_PRICE, VALID_CATEGORY)
    all_foods = food_service.get_all_food()
    food = [f for f in all_foods if f.name == VALID_NAME and f.price == VALID_PRICE][0]
    yield food
    food_service.delete_food(food.id)


'''
# -------------------------
# INPUT VALIDÁCIÓS TESZTEK
# -------------------------
'''

def test_create_food_missing_name():
    description = "Étel létrehozása név nélkül"
    expected = "Hiba: name is required"
    try:
        food_service.create_food("", VALID_DESCRIPTION, VALID_IMAGE, VALID_PRICE, VALID_CATEGORY)
        actual = "Sikerült létrehozni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "name is required" in actual
    report_result(description, expected, actual, match)
    assert match

def test_create_food_long_name():
    description = "Étel létrehozása túl hosszú névvel"
    expected = "Hiba: Food name must be 50 characters or fewer"
    long_name = "A" * 51
    try:
        food_service.create_food(long_name, VALID_DESCRIPTION, VALID_IMAGE, VALID_PRICE, VALID_CATEGORY)
        actual = "Sikerült létrehozni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "50 characters or fewer" in actual
    report_result(description, expected, actual, match)
    assert match

def test_create_food_negative_price():
    description = "Étel létrehozása negatív árral"
    expected = "Hiba: price must be a non-negative integer"
    try:
        food_service.create_food(VALID_NAME, VALID_DESCRIPTION, VALID_IMAGE, -100, VALID_CATEGORY)
        actual = "Sikerült létrehozni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "non-negative integer" in actual
    report_result(description, expected, actual, match)
    assert match

def test_create_food_long_category():
    description = "Étel létrehozása túl hosszú kategóriával"
    expected = "Hiba: Category must be 50 characters or fewer"
    long_category = "B" * 51
    try:
        food_service.create_food(VALID_NAME, VALID_DESCRIPTION, VALID_IMAGE, VALID_PRICE, long_category)
        actual = "Sikerült létrehozni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "50 characters or fewer" in actual
    report_result(description, expected, actual, match)
    assert match

def test_get_food_invalid_id():
    description = "Étel lekérdezése érvénytelen ID-val"
    expected = "Hiba: food_id must be a positive integer"
    try:
        food_service.get_food(-1)
        actual = "Sikerült lekérdezni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "positive integer" in actual
    report_result(description, expected, actual, match)
    assert match

def test_delete_food_invalid_id():
    description = "Étel törlése érvénytelen ID-val"
    expected = "Hiba: food_id must be a positive integer"
    try:
        food_service.delete_food("abc")
        actual = "Sikerült törölni"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "positive integer" in actual
    report_result(description, expected, actual, match)
    assert match

def test_update_food_nonexistent():
    description = "Nem létező étel módosítása"
    expected = "Hiba: Food with ID 99999 does not exist"

    try:
        food_service.update_food(
            99999,
            "Nem létező", "Leírás", "img.jpg", 1000, "Kategória"
        )
        actual = "Sikerült módosítani"
        match = False
    except ValueError as e:
        actual = str(e)
        match = "does not exist" in actual
    report_result(description, expected, actual, match)
    assert match


'''
# -------------------------
# LÉTREHOZÁS, MÓDOSÍTÁS, TÖRLÉS TESZTEK
# -------------------------
'''

def test_create_food_success():
    description = "Sikeres étel létrehozás"
    expected = "Étel létrejött és lekérdezhető"
    found = []

    try:
        food_service.create_food(VALID_NAME, VALID_DESCRIPTION, VALID_IMAGE, VALID_PRICE, VALID_CATEGORY)
        all_foods = food_service.get_all_food()
        found = [f for f in all_foods if f.name == VALID_NAME and f.price == VALID_PRICE]
        actual = f"Talált: {found[0].name}, {found[0].price}" if found else "Nem található"
        match = len(found) > 0
    except Exception as e:
        actual = str(e)
        match = False
    finally:
        if found:
            food_service.delete_food(found[0].id)
    report_result(description, expected, actual, match)
    assert match


def test_update_food_success():
    description = "Sikeres étel módosítás"
    expected = "Étel adatai frissültek"

    try:
        food_service.create_food("Frissítendő", "Leírás", "img.jpg", 1000, "Kategória")
        all_foods = food_service.get_all_food()
        food = [f for f in all_foods if f.name == "Frissítendő"][0]
        food_service.update_food(food.id, "Frissített név", "Új leírás", "img2.jpg", 1500, "Új kategória")
        updated = food_service.get_food(food.id)
        actual = f"{updated.name}, {updated.price}, {updated.category}"
        match = updated.name == "Frissített név" and updated.price == 1500 and updated.category == "Új kategória"
    except Exception as e:
        actual = str(e)
        match = False
    finally:
        if 'food' in locals():
            food_service.delete_food(food.id)
    report_result(description, expected, actual, match)
    assert match



def test_delete_food_success():
    description = "Sikeres étel törlés"
    expected = "Étel törölve, nem található többé"

    try:
        food_service.create_food("Törlendő", "Leírás", "img.jpg", 800, "Kategória")
        all_foods = food_service.get_all_food()
        food = [f for f in all_foods if f.name == "Törlendő"][0]
        food_service.delete_food(food.id)
        result = food_service.get_food(food.id)
        actual = "None" if result is None else f"Még létezik: {result.name}"
        match = result is None
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

'''
# -------------------------
# LISTA TESZT
# -------------------------
'''

def test_get_all_food_returns_list():
    description = "Összes étel lekérdezése"
    expected = "Lista visszatér, minden elem Food típusú"
    try:
        foods = food_service.get_all_food()
        actual = f"Talált {len(foods)} étel"
        match = isinstance(foods, list) and all(isinstance(f, Food) for f in foods)
    except Exception as e:
        actual = str(e)
        match = False
    report_result(description, expected, actual, match)
    assert match

'''
# -------------------------
# FIXTURE TESZT
# -------------------------
'''

def test_food_is_retrievable(test_food):
    description = "Tesztétel lekérdezhető"
    expected = "Lekérdezett étel megegyezik a létrehozottal"

    try:
        retrieved = food_service.get_food(test_food.id)
        actual = f"{retrieved.name}, {retrieved.price}"
        match = (
            retrieved is not None and
            retrieved.name == VALID_NAME and
            retrieved.price == VALID_PRICE
        )
    except Exception as e:
        actual = str(e)
        match = False

    report_result(description, expected, actual, match)
    assert match


def test_food_in_all_food_list(test_food):
    description = "Tesztétel szerepel az összes étel listában"
    expected = "get_all_food() tartalmazza a létrehozott ételt"

    try:
        all_foods = food_service.get_all_food()
        found = any(f.id == test_food.id for f in all_foods)
        actual = f"Szerepel: {test_food.name}" if found else "Nem szerepel"
        match = found
    except Exception as e:
        actual = str(e)
        match = False

    report_result(description, expected, actual, match)
    assert match

