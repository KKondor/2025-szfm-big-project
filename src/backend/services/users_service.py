from typing import Union
from repository.users import UserManager, User, Role

class UserService:

    """
    Service layer for managing user-related operations, including retrieval and role updates.
    Performs input validation and error handling.
    """

    def __init__(self):
        self._user_manager = UserManager()

    def get_all_users(self) -> list[User]:

        """
        Retrieves all users from the database.

        Returns:
            List[User]: A list of all users.

        Raises:
            RuntimeError: If the database operation fails.
        """

        try:
            return self._user_manager.get_all_user()
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve users: {e}")

#------------------------------
    def change_user_role(self, user_id: int, new_role: Role) -> str:
        
        """
        Updates the role of a specific user.

        Parameters:
            user_id (int): ID of the user whose role is to be updated.
            new_role (Role): New role to assign (Role.USER or Role.ADMIN).

        Raises:
            ValueError: If inputs are invalid or user does not exist.
            RuntimeError: If the database operation fails.
        """

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("user_id must be a positive integer")
        if not isinstance(new_role, Role):
            raise ValueError("new_role must be a valid Role enum value")

        try:
            user = self._user_manager.get_user_by_id(user_id)
            if user is None:
                raise ValueError(f"User with ID {user_id} does not exist")

            self._user_manager.update_user_role(user_id, new_role)
        except Exception as e:
            raise RuntimeError(f"Failed to update role for user {user_id}: {e}")


# Shared instance
user_service = UserService()
