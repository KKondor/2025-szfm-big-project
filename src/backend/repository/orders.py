from db_connect import get_connection
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from foods import Food
from users import User
import json

@dataclass
class OrderItem:
    item_id: int
    food: Food
    quantity: int
    item_price: int
    

@dataclass
class Order:
    order_id: int
    user: User
    order_date: datetime
    status: str
    note: Optional[str]
    total_price: int
    items: List[OrderItem]

class OrderManager:

#Új rendelést hoz létre az adatbázisba
#Meg kell adani neki bemenetbe:
#a felhasználó id, a megrendelt ételek id listában(egy étel többször is szerepelhet), a megjegyzést
    def create_order(self, user_id: int, food_ids: list, note: str):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            food_ids_json = json.dumps(food_ids)
            cursor.callproc("create_order", [user_id, food_ids_json, note])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

