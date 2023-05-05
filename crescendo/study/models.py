from core.factory.extensions import db
from core.models.base_model import BaseModel
from core.models.mixins import TimeStampedMixin, UUIDMixin


class StudyModel(BaseModel, TimeStampedMixin, UUIDMixin):
    __tablename__ = "study"

    name = db.Column(db.String(80), nullable=False)
    member_set = db.relationship("UserModel", backref="study")
