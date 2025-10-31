from enum import Enum
from dataclasses import dataclass
from typing import Optional
from db_connect import get_connection


class Role(Enum):
    USER = "user"
    ADMIN = "admin"

@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    role: Role

class UserManager:

#Új felhasználót hoz létre az adatbázisba
#Meg kell adani neki bemenetbe:
#a nevet, az email címet, és a jelszót már titkosított formában
#Alap értelmezetten user jogot ad a felhasználónak
    def create_user(self, name: str, email: str, password: str):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("create_user", [name, email, password, Role.USER.value])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

#Lecseréli egy adott felhasználó jelszavát
#Megkapja bemenetbe:
#az email címet, hogy melyík felhasználót kell módosítania
#és megkapja az új jelszót már titkosított formában
    def update_user_password(self, email: str, new_password: str):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("update_user_password", [email, new_password])
            conn.commit()
        finally:
            cursor.close()
            conn.close()
