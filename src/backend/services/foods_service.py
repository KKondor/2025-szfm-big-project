from typing import List, Optional

from repository.foods import FoodManager, Food

class FoodService:
    def __init__(self):
        self._food_manager = FoodManager()

    # Passthroughs with small validation
    def create_food(self, name: str, description: Optional[str], image: Optional[str], price: int, category: Optional[str]):
        if not name:
            raise ValueError("name is required")
        if price is None or price < 0:
            raise ValueError("price must be a non-negative integer")
        return self._food_manager.create_food(name, description, image, price, category)

    def delete_food(self, food_id: int):
        return self._food_manager.delete_food(food_id)

    def update_food(self, food_id: int, name: str, description: Optional[str], image: Optional[str], price: int, category: Optional[str]):
        if not name:
            raise ValueError("name is required")
        return self._food_manager.update_food(food_id, name, description, image, price, category)

    def get_food(self, food_id: int) -> Optional[Food]:
        return self._food_manager.get_food(food_id)

    def get_all_food(self) -> List[Food]:
        return self._food_manager.get_all_food()


# shared instance
food_service = FoodService()
