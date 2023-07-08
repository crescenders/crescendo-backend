from fullask_rest_framework.db import BaseModel, TimeStampedMixin, UUIDMixin
from fullask_rest_framework.factory.extensions import db


class CategoryModel(BaseModel):
    __tablename__ = "STUDY_CATEGORY"

    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"CategoryModel object <id:{self.id}, name:{self.name}>"


class TagModel(BaseModel):
    __tablename__ = "STUDY_TAG"

    name = db.Column(db.String(10))

    def __repr__(self) -> str:
        return f"TagModel object <id:{self.id}, name:{self.name}>"


class StudyGroupModel(BaseModel, TimeStampedMixin, UUIDMixin):
    __tablename__ = "STUDY_STUDYGROUP"

    # Foreign Keys
    leader_id = db.Column(
        db.Integer,
        db.ForeignKey("AUTH_USER.id", ondelete="CASCADE"),
        nullable=False,
    )
    # relationships
    leader = db.relationship("UserModel", backref="study_set")

    name = db.Column(db.String(80), nullable=False)
    user_limit = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def __repr__(self) -> str:
        return f"StudyGroupModel object <id:{self.id}, name:{self.name}>"


class RecruitmentPostModel(BaseModel, TimeStampedMixin, UUIDMixin):
    __tablename__ = "STUDY_RECRUITMENT_POST"

    # Foreign Keys
    studygroup_id = db.Column(
        db.Integer,
        db.ForeignKey("STUDY_STUDYGROUP.id", ondelete="CASCADE"),
        nullable=False,
    )
    # relationships
    studygroup = db.relationship("StudyGroupModel", backref="recruitment_post")
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.String(3000), nullable=False)
    deadline = db.Column(db.Date)

    def __repr__(self) -> str:
        return f"RecruitmentPostModel object <id:{self.id}, name:{self.title}>"


class RecruitmentHistoryModel(BaseModel):
    __tablename__ = "STUDY_RECRUITMENT_HISTORY"
    # Foreign Keys
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("AUTH_USER.id", ondelete="CASCADE"),
        nullable=False,
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("STUDY_RECRUITMENT_POST.id", ondelete="CASCADE"),
        nullable=False,
    )

    content = db.String(500)
    approval_status = db.Boolean()
    created_at = db.Column(
        db.DateTime, default=db.func.now(timezone=True), nullable=False
    )

    def __repr__(self) -> str:
        return f"RecruitmentHistoryModel object <id:{self.id}, name:{self.title}>"


class TagToStudyGroup(db.Model):
    __tablename__ = "STUDY_TAG_TO_STUDYGROUP"

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("STUDY_TAG.id", ondelete="CASCADE"),
        primary_key=True,
    )
    studygroup_id = db.Column(
        db.Integer,
        db.ForeignKey("STUDY_STUDYGROUP.id", ondelete="CASCADE"),
        primary_key=True,
    )


class CategoryToStudyGroup(db.Model):
    __tablename__ = "STUDY_CATEGORY_TO_STUDYGROUP"

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("STUDY_CATEGORY.id", ondelete="CASCADE"),
        primary_key=True,
    )
    studygroup_id = db.Column(
        db.Integer,
        db.ForeignKey("STUDY_STUDYGROUP.id", ondelete="CASCADE"),
        primary_key=True,
    )


class StudyGroupToUser(db.Model):
    __tablename__ = "STUDY_CATEGORY_TO_USER"

    studygroup_id = db.Column(
        db.Integer,
        db.ForeignKey("STUDY_STUDYGROUP.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("AUTH_USER.id", ondelete="CASCADE"),
        primary_key=True,
    )
