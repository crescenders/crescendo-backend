import abc

from core.extensions import db
from core.models.sqlalchemy.basemodel import BaseModel
from core.models.sqlalchemy.mixins import TimeStampedMixin, UUIDMixin


class User(BaseModel, TimeStampedMixin, UUIDMixin):
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(10), unique=True, nullable=False)
    first_name = db.Column(db.String(4), nullable=False)
    last_name = db.Column(db.String(4), nullable=False)
    gender = db.Column(db.Enum("남자", "여자"), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<id:{self.id}, full_name:{self.full_name}>"
