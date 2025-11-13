from typing import Union
from backend.repository.users import UserManager, User, Role

user_manager = UserManager()

# Visszaadja az összes felhasználó adatait
# Siker esetén egy listát ad vissza User objektumokkal
# Hiba esetén egy hibaüzenetet tartalmazó szöveget
from backend.repository.users import User


def get_all_users() -> Union[list[User], str]:
    try:
        users = user_manager.get_all_user()
        print(f"{len(users)} felhasználó betöltve.")
        return users
    except Exception as e:
        print(f"Hiba történt a felhasználók lekérdezése során: {e}")
        return "Hiba a felhasználók lekérdezése során"

#Megváltoztatja egy felhasználó jogosultságát
#Bemenetként megkapja:
#A felhasználó id, az új jogosultság: USER/ADMIN
#Ellenörzi, hogy létezik e az dott felhasználó
def change_user_role(user_id: int, new_role: Role) -> str:
    try:
        # Ellenőrzés: létezik-e a felhasználó
        all_users = user_manager.get_all_user()
        user = next((u for u in all_users if u.id == user_id), None)

        if not user:
            print("A megadott felhasználó nem létezik.")
            return "A megadott felhasználó nem létezik."

        # Jogosultság módosítása
        user_manager.update_user_role(user_id, new_role)
        print(f"A felhasználó (ID: {user_id}) jogosultsága sikeresen módosítva: {new_role.value}")
        return "A jogosultság sikeresen módosítva."
    except Exception as e:
        print(f"Hiba történt a jogosultság módosítása során: {e}")
        return "Hiba a jogosultság módosítása során"