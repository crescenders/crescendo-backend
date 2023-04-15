from enum import Enum

from core.extensions import db
from core.models.base_model import BaseModel
from core.models.mixins import TimeStampedMixin, UUIDMixin


class Roles(Enum):
    ADMIN = 0
    STAFF = 1
    USER = 2


class UserModel(BaseModel, TimeStampedMixin, UUIDMixin):
    __tablename__ = "user"

    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(10), unique=True, nullable=False)
    role = db.Column(db.Enum(Roles), nullable=False, server_default="USER")

    def __repr__(self) -> str:
        return f"<id:{self.id}, username:{self.username}>"
