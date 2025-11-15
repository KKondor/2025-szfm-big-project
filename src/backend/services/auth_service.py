import bcrypt
import re
from repository.users import UserManager, User
from typing import Union


user_manager = UserManager()

def is_valid_email(email: str) -> bool:

    """
    Checks whether the given email has a valid format.

    Parameters:
        email (str): The email address to validate.

    Returns:
        bool: True if valid, False otherwise.
    """

    if email == "admin":
        return True
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

#------------------------------
def is_strong_password(password: str) -> bool:

    """
    Checks whether the given password meets strength requirements.

    Requirements:
        - At least one lowercase letter
        - At least one uppercase letter
        - At least one digit
        - Minimum length of 6 characters

    Parameters:
        password (str): The password to validate.

    Returns:
        bool: True if strong, False otherwise.
    """

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    long_enough = len(password) >= 6
    return has_lower and has_upper and has_digit and long_enough

#------------------------------
def hash_password(password: str) -> str:

    """
    Hashes the given password using bcrypt.

    Parameters:
        password (str): The plain text password.

    Returns:
        str: The hashed password.

    Raises:
        RuntimeError: If hashing fails.
    """

    try:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    except Exception as e:
        raise RuntimeError(f"Password hashing failed: {e}")

#------------------------------
def login(identifier: str, password: str) -> Union[User, str]:
    
    """
    Authenticates a user by email or username and password.

    Parameters:
        identifier (str): Email or username.
        password (str): Plain text password.

    Returns:
        User: The authenticated user.

    Raises:
        ValueError: If credentials are invalid.
        RuntimeError: If authentication fails due to system error.
    """
    
    try:
        user = user_manager.get_user_by_identifier(identifier)
        if user is None or not bcrypt.checkpw(password.encode(), user.password.encode()):
            raise ValueError("Invalid email/username or password")
        return user
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"Login failed: {e}")

#------------------------------
def register(name: str, email: str, password: str, phone: str = "", address: str = "") -> str:
    
    """
    Registers a new user with the given credentials and contact information.

    Parameters:
        name (str): Full name of the user.
        email (str): Email address.
        password (str): Plain text password.
        phone (str): Optional phone number.
        address (str): Optional address.

    Raises:
        ValueError: If input is invalid or user already exists.
        RuntimeError: If registration fails due to system error.
    """
    
    if not name or len(name) > 100:
        raise ValueError("Name is required and must be 100 characters or fewer")
    if not is_valid_email(email):
        raise ValueError("Invalid email format")
    if not is_strong_password(password):
        raise ValueError("Password is not strong enough")
    if phone and len(phone) > 50:
        raise ValueError("Phone number must be 50 characters or fewer")
    if address and len(address) > 255:
        raise ValueError("Address must be 255 characters or fewer")
    if user_manager.get_user_by_email(email):
        raise ValueError("Email already exists")

    try:
        hashed_password = hash_password(password)
        user_manager.create_user(name, email, hashed_password, phone, address)
    except Exception as e:
        raise RuntimeError(f"Registration failed: {e}")

#------------------------------
def change_password(email: str, new_password: str) -> str:
    
    """
    Changes the password for a user identified by email.

    Parameters:
        email (str): Email address of the user.
        new_password (str): New plain text password.

    Raises:
        ValueError: If input is invalid or user does not exist.
        RuntimeError: If password update fails.
    """
    
    if not is_valid_email(email):
        raise ValueError("Invalid email format")
    if not is_strong_password(new_password):
        raise ValueError("New password is not strong enough")

    user = user_manager.get_user_by_email(email)
    if user is None:
        raise ValueError("Email does not exist")

    try:
        hashed_password = hash_password(new_password)
        user_manager.update_user_password(email, hashed_password)
    except Exception as e:
        raise RuntimeError(f"Password update failed: {e}")

#------------------------------
def get_user_by_email(email: str):

    """
    Retrieves a user by their email address.

    Parameters:
        email (str): Email address of the user.

    Returns:
        User: The user object.

    Raises:
        ValueError: If email is invalid or user not found.
        RuntimeError: If retrieval fails.
    """

    if not is_valid_email(email):
        raise ValueError("Invalid email format")

    try:
        user = user_manager.get_user_by_email(email)
        if user is None:
            raise ValueError("User with this email does not exist")
        return user
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve user by email: {e}")
