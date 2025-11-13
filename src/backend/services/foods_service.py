from typing import List, Optional
from repository.foods import FoodManager, Food

class FoodService:

    """
    Service layer for managing food-related operations, including creation, update, deletion,
    and retrieval of food items. Performs input validation and error handling.
    """

    def __init__(self):
        self._food_manager = FoodManager()

#------------------------------
    def create_food(self, name: str, description: Optional[str], image: Optional[str], price: int, category: Optional[str]):

        """
        Creates a new food item in the database.

        Parameters:
            name (str): Name of the food (required, max 50 characters).
            description (Optional[str]): Description of the food.
            image (Optional[str]): URL or path to the food image.
            price (int): Price of the food (non-negative integer).
            category (Optional[str]): Category of the food (max 50 characters).

        Raises:
            ValueError: If any input is invalid.
            RuntimeError: If the database operation fails.
        """

        if not name:
            raise ValueError("name is required")
        if len(name) > 50:
            raise ValueError("Food name must be 50 characters or fewer")
        if price is None or price < 0:
            raise ValueError("price must be a non-negative integer")
        if category and len(category) > 50:
            raise ValueError("Category must be 50 characters or fewer")

     
        try:
            self._food_manager.create_food(name, description, image, price, category)
        except Exception as e:
            raise RuntimeError(f"Failed to create food item: {e}")


#------------------------------
    def delete_food(self, food_id: int):

        """
        Deletes a food item from the database by its ID.

        Parameters:
            food_id (int): ID of the food to delete.

        Raises:
            ValueError: If the ID is invalid or the food does not exist.
            RuntimeError: If the database operation fails.
        """

        if not isinstance(food_id, int) or food_id <= 0:
            raise ValueError("food_id must be a positive integer")

        if self._food_manager.get_food(food_id) is None:
            raise ValueError(f"Food with ID {food_id} does not exist")

        try:
            self._food_manager.delete_food(food_id)
        except Exception as e:
            raise RuntimeError(f"Failed to delete food item with ID {food_id}: {e}")

#------------------------------
    def update_food(self, food_id: int, name: str, description: Optional[str], image: Optional[str], price: int, category: Optional[str]):
        
        """
        Updates an existing food item in the database.

        Parameters:
            food_id (int): ID of the food to update.
            name (str): New name of the food (required, max 50 characters).
            description (Optional[str]): New description.
            image (Optional[str]): New image URL or path.
            price (int): New price (non-negative integer).
            category (Optional[str]): New category (max 50 characters).

        Raises:
            ValueError: If any input is invalid or the food does not exist.
            RuntimeError: If the database operation fails.
        """

        if not isinstance(food_id, int) or food_id <= 0:
            raise ValueError("food_id must be a positive integer")
        if not name:
            raise ValueError("name is required")
        if len(name) > 50:
            raise ValueError("Food name must be 50 characters or fewer")
        if price is None or price < 0:
            raise ValueError("price must be a non-negative integer")
        if category and len(category) > 50:
            raise ValueError("Category must be 50 characters or fewer")

        if self._food_manager.get_food(food_id) is None:
            raise ValueError(f"Food with ID {food_id} does not exist")

        try:
            self._food_manager.update_food(food_id, name, description, image, price, category)
        except Exception as e:
            raise RuntimeError(f"Failed to update food item with ID {food_id}: {e}")

#------------------------------
    def get_food(self, food_id: int) -> Optional[Food]:

        """
        Retrieves a single food item by its ID.

        Parameters:
            food_id (int): ID of the food to retrieve.

        Returns:
            Optional[Food]: The food item if found, otherwise None.

        Raises:
            ValueError: If the ID is invalid.
            RuntimeError: If the database operation fails.
        """

        if not isinstance(food_id, int) or food_id <= 0:
            raise ValueError("food_id must be a positive integer")

        try:
            return self._food_manager.get_food(food_id)
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve food item with ID {food_id}: {e}")

#------------------------------
    def get_all_food(self) -> List[Food]:

        """
        Retrieves all food items from the database.

        Returns:
            List[Food]: A list of all food items.

        Raises:
            RuntimeError: If the database operation fails.
        """

        try:
            return self._food_manager.get_all_food()
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve food items: {e}")


# shared instance
food_service = FoodService()
