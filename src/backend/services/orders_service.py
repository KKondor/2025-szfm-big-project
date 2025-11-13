from typing import List
from repository.orders import OrderManager, Order, OrderStatus
from repository.foods import FoodManager
from repository.users import UserManager


class OrderService:
    def __init__(self):
        self._order_manager = OrderManager()
        self._food_manager = FoodManager()
        self._user_manager = UserManager()

#Létrehoz egy rendelést az adatbázisban az orders és order_items táblákban
#Bemenetben megkapja:
#felhasználó id, az ételek id listában, megjegyzés
    def create_order(self, user_id: int, food_ids: List[int], note: str = "") -> None:
        """Create a new order with validation."""
        if not isinstance(food_ids, list) or len(food_ids) == 0:
            raise ValueError("food_ids must be a non-empty list of food ids")

        # Validate each food exists
        for fid in food_ids:
            if self._food_manager.get_food(fid) is None:
                raise ValueError(f"food id {fid} does not exist")

        try:
            self._order_manager.create_order(user_id, food_ids, note)
        except Exception as e:
            raise RuntimeError(f"Failed to create order: {e}")

#Visszaadja az összes rendelés összes adatát listában Order
    def get_all_orders(self) -> List[Order]:
        """Retrieve all orders from the database."""
        
        try:
            return self._order_manager.get_all_orders()
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve orders: {e}")

#Visszaadja egy felhasználóhoz tartozó rendelések összes adatát listában Order
#Bemenetben megkapja: felhasználó id
    def get_order_by_user_id(self, user_id: int) -> List[Order]:
        """Retrieve all orders for a specific user."""
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("user_id must be a positive integer")

        try:
            return self._order_manager.get_order_by_user_id(user_id)
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve orders for user {user_id}: {e}")

#Módosítja egy rendeléshez tartozó állapotot
#Bemenetben megkapja:
#a rendelés id, az új stazuszt OrderStatus ENUM formában
    def update_order_status(self, order_id: int, new_status: OrderStatus) -> None:
        """Update the status of an existing order."""
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("order_id must be a positive integer")

        try:
            self._order_manager.update_order_status(order_id, new_status.value)
        except Exception as e:
            raise RuntimeError(f"Failed to update order status for order {order_id}: {e}")


# Shared instance
order_service = OrderService()
