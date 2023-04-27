from abc import ABC, abstractmethod

from core.repositories.crud import CRUDRepositoryABC


class FilteringRepositoryABC(CRUDRepositoryABC, ABC):
    pass


class SortingRepositoryABC(CRUDRepositoryABC, ABC):
    pass


class PaginationRepositoryABC(CRUDRepositoryABC, ABC):
    pass


class FilteringSortingPaginationRepository(
    FilteringRepositoryABC, SortingRepositoryABC, PaginationRepositoryABC, ABC
):
    pass
