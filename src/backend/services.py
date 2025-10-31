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


#Bejelentkezés email cím és jelszó kapott adatokkal.
#Ha a bejelentkezés sikeres akkor visszaadja a felhasználó adatait users.py User class alapján.
#Ha a bejelentkezés sikertelen akkor egy szöveget ad vissza.
def login(email: str, password: str) -> str:
    try:
        user = user_manager.get_user_by_email(email)
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            print("Bejelentkezés sikeres.")
            return user
        print("Bejelentkezés sikertelen: téves email vagy jelszó.")
        return "Bejelentkezés sikertelen: téves email vagy jelszó."
    except Exception as e:
        print(f"Hiba történt a bejelentkezés során: {e}")
        return "Hiba a bejelentkezés során"


#A regisztráció kapott adatai: név, email, jelszó
#Ellenörzi az email formátumát, a jelszó erősségét.
#Titkosítja a jelszót.
#Hozzáadja a felhasználót az adatbázishoz.
#Visszatérési érték pedig egy szöveg:
#a sikeres regisztrációról vagy esetleges hibákról
def register(name: str, email: str, password: str) -> str:
    try:
        if not is_valid_email(email):
            print("Hibás email formátum.")
            return "Hibás email formátum."

        if not is_strong_password(password):
            print("A jelszó nem elég erős.")
            return "A jelszó nem elég erős."

        if user_manager.get_user_by_email(email):
            print("Ilyen email már létezik.")
            return "Ilyen email már létezik."

        hashed_password = hash_password(password)
        if "Hiba" in hashed_password:
            return hashed_password

        user_manager.create_user(name, email, hashed_password)
        print("Regisztráció sikeres.")
        return "Regisztráció sikeres."
    except Exception as e:
        print(f"Hiba történt a regisztráció során: {e}")
        return "Hiba a regisztráció során"


#A jelszó megváltoztatásához szügséges adatok:
#az email cím, az új jelszó
#Ellenörni, hogy az új jelszó elég erős e.
#Ellenörni, hogy a megadott email cím létezik e.
#Titkosítja az új jelszót és kicseréli az adatbázisban.
#Visszatérési érték pedig egy szöveg:
#a sikeres jelszó módosításról vagy esetleges hibákról
def change_password(email: str, new_password: str) -> str:
    try:
        if not is_strong_password(new_password):
            print("A jelszó nem elég erős.")
            return "A jelszó nem elég erős."

        user = user_manager.get_user_by_email(email)
        if not user:
            print("Az email nem létezik.")
            return "Az email nem létezik."

        hashed_password = hash_password(new_password)
        if "Hiba" in hashed_password:
            return hashed_password

        user_manager.update_user_password(email, hashed_password)
        print("A jelszó sikeresen megváltozott.")
        return "A jelszó sikeresen megváltozott."
    except Exception as e:
        print(f"Hiba történt a jelszó módosítása során: {e}")
        return "Hiba a jelszó módosítása során"
