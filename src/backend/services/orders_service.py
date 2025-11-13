from typing import List
from repository.orders import OrderManager, Order, OrderStatus
from repository.foods import FoodManager
from repository.users import UserManager

class OrderService:

    """
    Service layer for managing order-related operations, including creation, retrieval,
    and status updates. Performs input validation and error handling.
    """

    def __init__(self):
        self._order_manager = OrderManager()
        self._food_manager = FoodManager()
        self._user_manager = UserManager()


#------------------------------
    def create_order(self, user_id: int, food_ids: List[int], note: str = "") -> None:

        """
        Creates a new order in the database.

        Parameters:
            user_id (int): ID of the user placing the order.
            food_ids (List[int]): List of food item IDs (can contain duplicates).
            note (str): Optional note attached to the order.

        Raises:
            ValueError: If inputs are invalid or food/user does not exist.
            RuntimeError: If the database operation fails.
        """

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("user_id must be a positive integer")
        if not isinstance(food_ids, list) or len(food_ids) == 0:
            raise ValueError("food_ids must be a non-empty list of food IDs")
        if note and len(note) > 500:
            raise ValueError("Note must be 500 characters or fewer")

        if self._user_manager.get_user_by_id(user_id) is None:
            raise ValueError(f"User with ID {user_id} does not exist")


        for fid in food_ids:
            if not isinstance(fid, int) or fid <= 0:
                raise ValueError(f"Invalid food ID: {fid}")
            if self._food_manager.get_food(fid) is None:
                raise ValueError(f"Food with ID {fid} does not exist")


        try:
            self._order_manager.create_order(user_id, food_ids, note)
        except Exception as e:
            raise RuntimeError(f"Failed to create order: {e}")


#------------------------------
    def get_all_orders(self) -> List[Order]:

        """
        Retrieves all orders from the database.

        Returns:
            List[Order]: A list of all orders.

        Raises:
            RuntimeError: If the database operation fails.
        """

        try:
            return self._order_manager.get_all_orders()
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve orders: {e}")


#------------------------------
    def get_order_by_user_id(self, user_id: int) -> List[Order]:

        """
        Retrieves all orders for a specific user.

        Parameters:
            user_id (int): ID of the user.

        Returns:
            List[Order]: A list of orders for the user.

        Raises:
            ValueError: If the user ID is invalid or user does not exist.
            RuntimeError: If the database operation fails.
        """

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("user_id must be a positive integer")

        if self._user_manager.get_user_by_id(user_id) is None:
            raise ValueError(f"User with ID {user_id} does not exist")

        try:
            return self._order_manager.get_order_by_user_id(user_id)
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve orders for user {user_id}: {e}")


#------------------------------
    def update_order_status(self, order_id: int, new_status: OrderStatus) -> None:

        """
        Updates the status of an existing order.

        Parameters:
            order_id (int): ID of the order to update.
            new_status (OrderStatus): New status to set.

        Raises:
            ValueError: If inputs are invalid.
            RuntimeError: If the database operation fails.
        """

        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("order_id must be a positive integer")

        if not isinstance(new_status, OrderStatus):
            raise ValueError("new_status must be a valid OrderStatus enum value")

        try:
            self._order_manager.update_order_status(order_id, new_status.value)
        except Exception as e:
            raise RuntimeError(f"Failed to update order status for order {order_id}: {e}")


# Shared instance
order_service = OrderService()
