from typing import Union
from repository.users import UserManager, User, Role

user_manager = UserManager()

# Wraps user operations
class UserService:
    def __init__(self):
        self._user_manager = UserManager()

    def get_all_users(self) -> Union[list[User], str]:
        try:
            users = self._user_manager.get_all_user()
            print(f"{len(users)} felhasználó betöltve.")
            return users
        except Exception as e:
            print(f"Hiba történt a felhasználók lekérdezése során: {e}")
            return "Hiba a felhasználók lekérdezése során"

    def change_user_role(self, user_id: int, new_role: Role) -> str:
        try:
            all_users = self._user_manager.get_all_user()
            user = next((u for u in all_users if u.id == user_id), None)

            if not user:
                print("A megadott felhasználó nem létezik.")
                return "A megadott felhasználó nem létezik."

            self._user_manager.update_user_role(user_id, new_role)
            print(f"A felhasználó (ID: {user_id}) jogosultsága sikeresen módosítva: {new_role.value}")
            return "A jogosultság sikeresen módosítva."
        except Exception as e:
            print(f"Hiba történt a jogosultság módosítása során: {e}")
            return "Hiba a jogosultság módosítása során"

# Shared instance
user_service = UserService()