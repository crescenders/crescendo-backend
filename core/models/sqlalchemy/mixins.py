from uuid import uuid4

from core.extensions import db


class BaseMixin:
    """모든 믹스인들의 부모 믹스인
    믹스인이 클래스 자체로 사용되지 못하도록 합니다."""

    def __init__(self, *args, **kwargs):
        if type(self) is self.__class__:
            raise TypeError(
                f"You can only use {self.__class__.__name__} for implementing Mixin."
            )
        super().__init__(*args, **kwargs)


class TimeStampedMixin(BaseMixin):
    """생성일자, 수정일자를 자동 저장하기 위한 믹스인"""

    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )


class UUIDMixin(BaseMixin):
    """UUID 필드를 더해주는 믹스인"""

    uuid = db.Column(db.String(36), unique=True, default=str(uuid4()), nullable=False)
