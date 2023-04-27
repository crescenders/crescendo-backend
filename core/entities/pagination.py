from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


@dataclass
class PaginationEntity(Generic[T]):
    # request
    request_page: int
    request_size: int

    # response
    count: int
    next_num: Optional[int]
    previous_num: Optional[int]
    results: List[T]
