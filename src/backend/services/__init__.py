"""
Services package initializer. Exposes ready-to-use service instances.
"""
from services.users_service import user_service
from services.foods_service import food_service
from services.orders_service import order_service
import services.auth_service as auth_service

users_service = user_service
foods_service = food_service
orders_service = order_service

__all__ = ["user_service", "food_service", "order_service", "auth_service", "users_service", "foods_service", "orders_service"]
