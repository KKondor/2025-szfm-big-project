import bcrypt
import re
from users import UserManager, User

user_manager = UserManager()

#Ellenörni, hogy a megadott email címnek helyes e a formátuma.
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


