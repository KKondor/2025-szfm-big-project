from repository.db_connect import get_connection
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from repository.foods import Food, FoodManager
from repository.users import User, UserManager
import json
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


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
    status: OrderStatus
    note: Optional[str]
    total_price: int
    items: List[OrderItem]

#------------------------------
class OrderManager:

    """
    Handles direct database operations related to orders and order items.
    """

#------------------------------
    def create_order(self, user_id: int, food_ids: list, note: str):
        
        """
        Creates a new order and inserts it into the orders and order_items tables.

        Parameters:
            user_id (int): ID of the user placing the order.
            food_ids (list): List of food item IDs (can contain duplicates).
            note (str): Optional note attached to the order.
        """

        conn = get_connection()
        cursor = conn.cursor()
        try:
            food_ids_json = json.dumps(food_ids)
            cursor.callproc("create_order", [user_id, food_ids_json, note])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

#------------------------------
    def get_all_orders(self) -> List[Order]:

        """
        Retrieves all orders from the database, including their items and associated user and food data.

        Returns:
            List[Order]: A list of all orders.
        """

        conn = get_connection()
        cursor = conn.cursor()
        orders_dict = {}
        try:
            cursor.callproc("get_all_orders")
            for result in cursor.stored_results():
                for row in result.fetchall():
                    order_id = row[0]
                    user_id = row[1]
                    order_date = row[2]
                    status = OrderStatus(row[3])
                    note = row[4]
                    total_price = row[5]
                    item_id = row[6]
                    food_id = row[7]
                    quantity = row[8]
                    item_price = row[9]

                    user = UserManager().get_user_by_id(user_id)
                    food = FoodManager().get_food(food_id)


                    if order_id not in orders_dict:
                        orders_dict[order_id] = Order(
                            order_id=order_id,
                            user=user,
                            order_date=order_date,
                            status=status,
                            note=note,
                            total_price=total_price,
                            items=[]
                        )

                    if food:
                        item = OrderItem(
                            item_id=item_id,
                            food=food,
                            quantity=quantity,
                            item_price=item_price
                        )
                        orders_dict[order_id].items.append(item)

            return list(orders_dict.values())
        finally:
            cursor.close()
            conn.close()

#------------------------------
    def get_order_by_user_id(self, user_id: int) -> List[Order]:

        """
        Retrieves all orders for a specific user.

        Parameters:
            user_id (int): ID of the user.

        Returns:
            List[Order]: A list of orders associated with the user.
        """

        conn = get_connection()
        cursor = conn.cursor()
        orders_dict = {}
        try:
            cursor.callproc("get_order_by_user_id", [user_id])
            for result in cursor.stored_results():
                for row in result.fetchall():
                    order_id = row[0]
                    order_date = row[2]
                    status = OrderStatus(row[3])
                    note = row[4]
                    total_price = row[5]
                    item_id = row[6]
                    food_id = row[7]
                    quantity = row[8]
                    item_price = row[9]

                    user = UserManager().get_user_by_id(user_id)
                    food = FoodManager().get_food(food_id)

                    if order_id not in orders_dict:
                        orders_dict[order_id] = Order(
                            order_id=order_id,
                            user=user,
                            order_date=order_date,
                            status=status,
                            note=note,
                            total_price=total_price,
                            items=[]
                        )

                    if food:
                        item = OrderItem(
                            item_id=item_id,
                            food=food,
                            quantity=quantity,
                            item_price=item_price
                        )
                        orders_dict[order_id].items.append(item)

            return list(orders_dict.values())
        finally:
            cursor.close()
            conn.close()

#------------------------------
    def update_order_status(self, order_id: int, new_status: OrderStatus):
        
        """
        Updates the status of an existing order.

        Parameters:
            order_id (int): ID of the order to update.
            new_status (OrderStatus): New status to assign.
        """

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("update_order_status", [order_id, new_status.value])
            conn.commit()
        finally:
            cursor.close()
            conn.close()
