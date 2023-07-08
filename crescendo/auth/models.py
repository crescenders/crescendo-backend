from fullask_rest_framework.db import BaseModel, TimeStampedMixin, UUIDMixin
from fullask_rest_framework.factory.extensions import db


class RoleModel(BaseModel):
    __tablename__ = "AUTH_ROLE"
    name = db.Column(db.String(15))

    def __repr__(self) -> str:
        return f"RoleModel object <id:{self.id}, name:{self.name}>"


class UserModel(BaseModel, TimeStampedMixin, UUIDMixin):
    __tablename__ = "AUTH_USER"

    # Foreign keys
    role_id = db.Column(db.Integer, db.ForeignKey("AUTH_ROLE.id"))
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(10), unique=False, nullable=False)

    # Relationships
    role = db.relationship("RoleModel", backref="user_set")

    def __repr__(self) -> str:
        return f"UserModel object <id:{self.id}, username:{self.username}>"
