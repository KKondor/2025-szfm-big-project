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
