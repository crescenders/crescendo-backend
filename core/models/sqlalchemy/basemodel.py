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
