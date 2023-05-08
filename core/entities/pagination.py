from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

from core.entities.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


@dataclass
class PaginationResponse(Generic[T]):
    count: Optional[int]
    next_page: Optional[int]
    previous_page: Optional[int]
    results: List


@dataclass
class PaginationRequest:
    page: int = None
    per_page: int = None
