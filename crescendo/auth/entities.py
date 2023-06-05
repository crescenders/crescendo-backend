from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from flask_jwt_extended import create_access_token, create_refresh_token
from fullask_rest_framework.entities.base_entity import BaseEntity


@dataclass
class UserEntity(BaseEntity):
    email: str
    role: str
    username: str
    id: Optional[int] = None
    uuid: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    study_id: Optional[int] = None  # foreign key

    @property
    def access_token(self):
        return create_access_token(
            identity=self.uuid, additional_claims={"role": self.role}
        )

    @property
    def refresh_token(self):
        return create_refresh_token(
            identity=self.uuid, additional_claims={"role": self.role}
        )


@dataclass
class JWTResponse(BaseEntity):
    access_token: str
    refresh_token: str
