from sqlalchemy.orm import validates

from core.factory.extensions import db
from core.models.base_model import BaseModel
from core.models.mixins import TimeStampedMixin, UUIDMixin


class UserModel(BaseModel, TimeStampedMixin, UUIDMixin):
    __tablename__ = "user"

    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(10), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False, server_default="USER")
    study_id = db.Column(db.Integer, db.ForeignKey("study.id"))

    def __repr__(self) -> str:
        return f"<id:{self.id}, username:{self.username}>"

    @validates("role")
    def validate_role(self, key, value):
        """role 컬럼에 대한 유효성 검사를 수행합니다."""
        valid_roles = ["USER", "STAFF", "ADMIN"]
        if value not in valid_roles:
            raise ValueError(
                f"{value} is not a valid role, valid roles are {valid_roles}"
            )
        return value
