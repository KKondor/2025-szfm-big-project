from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
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
    phone: Optional[str] = None
    address: str
    role: Role

class UserManager:

#Új felhasználót hoz létre az adatbázisba
#Meg kell adani neki bemenetbe:
#a nevet, az email címet, és a jelszót már titkosított formában
#Alap értelmezetten user jogot ad a felhasználónak
    def create_user(self, name: str, email: str, password: str, phone: str, address: str):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("create_user", [name, email, password, phone, address, Role.USER.value])
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

#Viszzaadja egy felhasználó összes adatát
#Bemenetkénk megkapja:
#a felhasználó email címét
#Ha az adatbázisban nem szerepel az adott email cím akkor None ad vissza
    def get_user_by_email(self, email: str) -> Optional[User]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("get_user_by_email", [email])
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    return User(
                        id=row[0],
                        name=row[1],
                        email=row[2],
                        password=row[3],
                        phone=row[4],
                        address=row[5],
                        role=Role(row[6])
                    )
            print("Nincs ilyen email című felhasználó")
            return None
        finally:
            cursor.close()
            conn.close()

#Viszzaadja egy felhasználó összes adatát
#Bemenetkénk megkapja:
#a felhasználó email címét vagy felhasználónevét
#Ha az adatbázisban nem szerepel az adott email cím és vagy felhasználónév akkor None ad vissza
    def get_user_by_identifier(self, identifier: str) -> Optional[User]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("get_user_by_identifier", [identifier])
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    return User(
                        id=row[0],
                        name=row[1],
                        email=row[2],
                        password=row[3],
                        address=row[4],
                        role=Role(row[5]),
                        phone=row[6] if row[6] is not None else None
                    )
            return None
        finally:
            cursor.close()
            conn.close()

#Visszaadja egy listában az összes felhasználót és azok összes adatát
    def get_all_user(self) -> List[User]:
        conn = get_connection()
        cursor = conn.cursor()
        users = []
        try:
            cursor.callproc("get_all_user")
            for result in cursor.stored_results():
                for row in result.fetchall():
                    user = User(
                        id=row[0],
                        name=row[1],
                        email=row[2],
                        password=row[3],
                        phone=row[4] if row[4] is not None else None,
                        address=row[5],
                        role=Role(row[6])
                    )
                    users.append(user)
            return users
        finally:
            cursor.close()
            conn.close()
