from typing import List

from repository.orders import OrderManager
from repository.foods import FoodManager


class OrderService:
    def __init__(self):
        self._order_manager = OrderManager()
        self._food_manager = FoodManager()

    def create_order(self, user_id: int, food_ids: List[int], note: str = "") -> None:
        """Create a new order with validation."""
        if not isinstance(food_ids, list) or len(food_ids) == 0:
            raise ValueError("food_ids must be a non-empty list of food ids")

        # Validate each food exists
        for fid in food_ids:
            if self._food_manager.get_food(fid) is None:
                raise ValueError(f"food id {fid} does not exist")

        self._order_manager.create_order(user_id, food_ids, note)


# Shared instance
order_service = OrderService()
