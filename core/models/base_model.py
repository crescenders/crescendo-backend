from core.extensions import db


class BaseModel(db.Model):  # type: ignore[name-defined]
    """모든 모델의 부모 모델"""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
