import bcrypt
import re
from users import UserManager, User

user_manager = UserManager()

#Ellenörni, hogy a megadott email címnek helyes e a formátuma.
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


#Ellenörzi, hogy a megadott jelszó elég erős e.
#Megnézi, hogy szerepel e benne: kis betű, nagy betű, szám
#És megnézi, hogy minimum tartalmaz e 12 karaktert.
def is_strong_password(password: str) -> bool:
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    long_enough = len(password) >= 12
    return has_lower and has_upper and has_digit and long_enough


#Titkosítja a megadott jelszót bcrypt hash algoritmussal.
def hash_password(password: str) -> str:
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print("A jelszó titkosítása elkészült.")
        return hashed
    except Exception as e:
        print(f"Hiba történt a jelszó titkosítása során: {e}")
        return "Hiba a jelszó titkosításakor"
