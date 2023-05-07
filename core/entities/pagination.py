from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PaginationResponse:
    count: Optional[int]
    next_page: Optional[int]
    previous_page: Optional[int]
    results: List
