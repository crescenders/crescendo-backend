from abc import ABC, abstractmethod


class BaseRepository(ABC):
    """
    모든 Repository 의 부모 Repository

    Service 에서 Model(ORM object) 를 직접적으로
    사용하지 않도록 데이터 조회에 대한 인터페이스를 정의합니다.
    """

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def get_all(self, **kwargs):
        pass

    @abstractmethod
    def get_one(self, **kwargs):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def count(self):
        pass
