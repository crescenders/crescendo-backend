from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


@dataclass
class PaginationResponseEntity(Generic[T]):
    count: int
    next_page: Optional[str]
    previous_page: Optional[str]
    results: List[T]
