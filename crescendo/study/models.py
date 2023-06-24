from fullask_rest_framework.factory.extensions import db
from fullask_rest_framework.orm.sqlalchemy.base_model import BaseModel
from fullask_rest_framework.orm.sqlalchemy.mixins import TimeStampedMixin, UUIDMixin


class CategoryModel(BaseModel):
    __tablename__ = "study_category"

    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False)


class StudyModel(BaseModel, TimeStampedMixin, UUIDMixin):
    __tablename__ = "study_study"

    name = db.Column(db.String(80), nullable=False)
    member_set = db.relationship("UserModel", backref="study")
