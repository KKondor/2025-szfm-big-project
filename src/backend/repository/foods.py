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

#Frissíti egy adott étel adatait az adatbázisban id alapján
#Bemenetként minden adatot meg kell neki adni azt is amit nem akarunk módosítani:
#az id, a nevet, a leírást, a kép liknjét, az ár, a típus
    def update_food(self, food_id: int, name: str, description: str, image: str, price: int, category: str):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("update_food", [food_id, name, description, image, price, category])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

#Visszaadja egy étel minden adatát az adatbázisból
#Bemenetkénk megkapja: id
    def get_food(self, food_id: int) -> Optional[Food]:
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

#Visszaadja az összes étel minden adatát az adatbázisból
#A visszatérési érték egy lista, melynek minden eleme egy Food
    def get_all_food(self) -> List[Food]:
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
