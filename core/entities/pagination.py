from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar("T")


class PaginationEntity(Generic[T]):
    def __init__(
        self,
        count: int,
        next_num: Optional[int],
        previous_num: Optional[int],
        results: List[T],
    ):
        self.count = count
        self.next_num = next_num
        self.previous_num = previous_num
        self.results = results
