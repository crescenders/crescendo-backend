from dataclasses import dataclass
from typing import List


@dataclass
class SortingEntity:
    """
    - 어떤 필드를 기준으로 정렬할 것인가?
    - 어떤 방향으로 정렬할 것인가?
    """

    fields: List[str]
