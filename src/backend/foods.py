from dataclasses import dataclass
from typing import Optional

@dataclass
class Food:
    id: int
    name: str
    description: Optional[str]
    image: Optional[str]
    price: int
    category: Optional[str]

class FoodManager:
    
#Új ételt hoz létre az adatbázisba
#Meg kell adani neki bemenetbe:
#a nevet, a leírást, a kép liknjét, az ár, a típus
    def create_food(self, name: str, description: str, image: str, price: int, category: str):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("create_food", [name, description, image, price, category])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

#Kitörli az adott ételt az adatbázisból
#Meg kell adani neki bemenetbe: id
    def delete_food(self, food_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("delete_food", [food_id])
            conn.commit()
        finally:
            cursor.close()
            conn.close()
