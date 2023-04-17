from abc import ABC, abstractmethod


class PaginationEntity(ABC):
    def __init__(self, count: int, next: int, previous: int):
        self.count = count
        self.next = next
        self.previous = previous

    @abstractmethod
    def set_results(self, results):
        pass
