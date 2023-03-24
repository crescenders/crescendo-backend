from typing import List

from core.extensions import db
from core.repositories.baserepository import BaseRepository
from crescenders.users.models import User


class UserRepository(BaseRepository):
    def __init__(self):
        self.model = User

    def create(self, **kwargs) -> User:
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user

    def get_all(self, **kwargs) -> List[User]:
        return self.model.query.all(**kwargs)

    def get_one(self, **kwargs) -> User:
        return self.model.query.get()

    def update(self) -> User:
        return self.model.query.update()

    def delete(self) -> None:
        return self.model.query.delete()

    def count(self) -> int:
        return self.model.query.count()
