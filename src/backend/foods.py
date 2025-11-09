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
