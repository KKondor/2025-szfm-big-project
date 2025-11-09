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
