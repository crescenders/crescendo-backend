from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseEntity:
    id: Optional[int]
