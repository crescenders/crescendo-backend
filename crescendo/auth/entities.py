from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


@dataclass
class UserEntity:
    id: Optional[int]
    uuid: Optional[str]
    email: str
    role: Enum
    username: str
    created_at: datetime
    updated_at: datetime
    study_id: Optional[int] = None  # foreign key
