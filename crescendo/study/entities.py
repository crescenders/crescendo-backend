from dataclasses import dataclass
from typing import Optional


@dataclass
class CategoryEntity:
    name: str
    description: str
    id: Optional[int] = None
