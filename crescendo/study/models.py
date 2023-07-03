from fullask_rest_framework.db.sqlalchemy.base_model import BaseModel
from fullask_rest_framework.db.sqlalchemy.mixins import TimeStampedMixin, UUIDMixin
from fullask_rest_framework.factory.extensions import db


class CategoryModel(BaseModel):
    __tablename__ = "study_category"

    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False)


class StudyModel(BaseModel, TimeStampedMixin, UUIDMixin):
    __tablename__ = "study_study"

    name = db.Column(db.String(80), nullable=False)
    member_set = db.relationship("UserModel", backref="study")
