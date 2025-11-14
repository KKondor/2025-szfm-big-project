from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
from repository.db_connect import get_connection


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

#------------------------------
class UserManager:

    """
    Handles direct database operations related to users.
    """

#------------------------------
    def create_user(self, name: str, email: str, password: str, phone: str, address: str):
        
        """
        Inserts a new user into the database.

        Parameters:
            name (str): Full name of the user.
            email (str): Email address.
            password (str): Hashed password.
            phone (str): Phone number.
            address (str): Address.
        """

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("create_user", [name, email, password, phone, address, Role.USER.value])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

#------------------------------
    def update_user_password(self, email: str, new_password: str):

        """
        Updates the password of a user identified by email.

        Parameters:
            email (str): Email address of the user.
            new_password (str): New hashed password.
        """

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("update_user_password", [email, new_password])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

#------------------------------
    def get_user_by_email(self, email: str) -> Optional[User]:

        """
        Retrieves a user by their email address.

        Parameters:
            email (str): Email address to search.

        Returns:
            Optional[User]: The user if found, otherwise None.
        """

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
                        phone=row[4] if row[4] is not None else None,
                        address=row[5],
                        role=Role(row[6])
                    )
            print("Nincs ilyen email című felhasználó")
            return None
        finally:
            cursor.close()
            conn.close()

#------------------------------
    def get_user_by_identifier(self, identifier: str) -> Optional[User]:

        """
        Retrieves a user by either email or username.

        Parameters:
            identifier (str): Email or username.

        Returns:
            Optional[User]: The user if found, otherwise None.
        """

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
                        phone=row[4] if row[4] is not None else None,
                        address=row[5],
                        role=Role(row[6])
                    )
            return None
        finally:
            cursor.close()
            conn.close()


#------------------------------
    def get_all_user(self) -> List[User]:

        """
        Retrieves all users from the database.

        Returns:
            list[User]: A list of all users.
        """

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


#------------------------------
    def get_user_by_id(self, user_id: int) -> Optional[User]:

        """
        Retrieves a user by their ID.

        Parameters:
            user_id (int): ID of the user.

        Returns:
            Optional[User]: The user if found, otherwise None.
        """

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("get_user_by_id", [user_id])
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    return User(
                        id=row[0],
                        name=row[1],
                        email=row[2],
                        password=row[3],
                        phone=row[4] if row[4] is not None else None,
                        address=row[5],
                        role=Role(row[6])
                    )
            return None
        finally:
            cursor.close()
            conn.close()

#------------------------------
    def update_user_role(self, user_id: int, new_role: Role):

        """
        Updates the role of a user.

        Parameters:
            user_id (int): ID of the user.
            new_role (Role): New role to assign.
        """

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("update_user_role", [user_id, new_role.value])
            conn.commit()
        finally:
            cursor.close()
            conn.close()


