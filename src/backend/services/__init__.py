"""
Services package initializer. Exposes ready-to-use service instances.
"""
from .users_service import user_service
from .foods_service import food_service
from .orders_service import order_service

__all__ = ["user_service", "food_service", "order_service"]
