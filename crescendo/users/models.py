from core.extensions import db
from core.models.base_model import BaseModel
from core.models.mixins import TimeStampedMixin, UUIDMixin


class UserModel(BaseModel, TimeStampedMixin, UUIDMixin):
    __tablename__ = "user"

    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<id:{self.id}, usernamee:{self.username}>"
