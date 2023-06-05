from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from core.entities.base_entity import BaseEntity


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
