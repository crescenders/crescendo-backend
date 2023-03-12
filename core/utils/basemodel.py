from uuid import uuid4

from core.extensions import db


class BaseModel(db.Model):
    """모든 모델의 부모 모델"""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    @property
    def __tablename__(cls):
        """기본 테이블 이름을 클래스명으로 지정"""
        return cls.__name__


class TimeStampedMixin:
    """생성일자, 수정일자를 자동 저장하기 위한 믹스인"""

    created_on = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_on = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )


class UUIDMixin:
    """UUID 필드를 더해주는 믹스인"""

    uuid = db.Column(db.String(36), unique=True, default=str(uuid4()), nullable=False)
