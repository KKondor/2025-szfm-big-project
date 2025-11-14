from repository.db_connect import get_connection
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Food:
    id: int
    name: str
    description: Optional[str]
    image: Optional[str]
    price: int
    category: Optional[str]

#------------------------------
class FoodManager:

    """
    Handles direct database operations related to food items.
    """

    def create_food(self, name: str, description: str, image: str, price: int, category: str):
        
        """
        Inserts a new food item into the database.

        Parameters:
            name (str): Name of the food.
            description (str): Description of the food.
            image (str): Image URL or path.
            price (int): Price of the food.
            category (str): Category of the food.
        """
        
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("create_food", [name, description, image, price, category])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

#------------------------------
    def delete_food(self, food_id: int):

        """
        Deletes a food item from the database by its ID.

        Parameters:
            food_id (int): ID of the food to delete.
        """

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("delete_food", [food_id])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

#------------------------------
    def update_food(self, food_id: int, name: str, description: str, image: str, price: int, category: str):
        
        """
        Updates an existing food item in the database.

        Parameters:
            food_id (int): ID of the food to update.
            name (str): New name.
            description (str): New description.
            image (str): New image URL or path.
            price (int): New price.
            category (str): New category.
        """
        
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("update_food", [food_id, name, description, image, price, category])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

#------------------------------
    def get_food(self, food_id: int) -> Optional[Food]:

        """
        Retrieves a single food item by its ID.

        Parameters:
            food_id (int): ID of the food to retrieve.

        Returns:
            Optional[Food]: The food item if found, otherwise None.
        """

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("get_food", [food_id])
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    return Food(
                        id=row[0],
                        name=row[1],
                        description=row[2],
                        image=row[3],
                        price=row[4],
                        category=row[5]
                    )
            return None
        finally:
            cursor.close()
            conn.close()

#------------------------------
    def get_all_food(self) -> List[Food]:

        """
        Retrieves all food items from the database.

        Returns:
            List[Food]: A list of all food items.
        """

        conn = get_connection()
        cursor = conn.cursor()
        foods = []
        try:
            cursor.callproc("get_all_food")
            for result in cursor.stored_results():
                rows = result.fetchall()
                for row in rows:
                    food = Food(
                        id=row[0],
                        name=row[1],
                        description=row[2],
                        image=row[3],
                        price=row[4],
                        category=row[5]
                    )
                    foods.append(food)
            return foods
        finally:
            cursor.close()
            conn.close()

