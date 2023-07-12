from fullask_rest_framework.schemas import PaginationResponseSchema
from marshmallow import Schema, fields


class AuthorSchema(Schema):
    """스터디 홍보글 저자의 정보를 나타내기 위해서 필요한 스키마입니다."""

    uuid = fields.UUID()
    username = fields.Str(
        metadata={
            "example": "Goddessana",
        },
    )
    email = fields.Email()


class CategorySchema(Schema):
    """카테고리 조회와 생성, 수정을 위해 필요한 스키마입니다."""

    id = fields.Int(required=False, dump_only=True)
    name = fields.Str(
        required=True,
        metadata={"description": "카테고리의 이름", "example": "CPython"},
    )
    description = fields.Str(
        required=True,
        metadata={
            "description": "CPython 카테고리입니다.",
        },
    )


class StudyGroupCreateSchema(Schema):
    """
    스터디그룹과 스터디그룹 홍보 게시물을 작성하기 위해서 필요한 스키마입니다.
    """

    name = fields.Str(
        required=True,
        metadata={
            "description": "개설하고자 하는 스터디의 이름",
            "example": "Make Django GREAT Again. DRF 스터디",
        },
    )
    user_limit = fields.Int(
        required=True,
        metadata={
            "description": "모집 멤버 수",
        },
    )
    start_date = fields.Date(
        required=True,
        metadata={
            "description": "스터디 시작일자",
        },
    )
    end_date = fields.Date(
        required=True,
        metadata={
            "description": "스터디 종료일자",
        },
    )
    deadline = fields.Date(required=True)
    title = fields.Str(
        required=True,
        metadata={
            "description": "스터디그룹 홍보 게시물의 제목",
            "example": "Django-REST-Framework 스터디를 모집합니다!",
        },
    )
    content = fields.Str(
        required=True,
        metadata={
            "description": "스터디그룹 홍보 게시물의 내용",
            "example": "DRF 는 Django 사용 시 거의 표준이 되었다고 해도 무방한 프레임워크가 되었습니다.. 같이 스터디 해요!",
        },
    )
    category_ids = fields.List(
        fields.Int(required=True),
        metadata={
            "description": "붙이고자 하는 카테고리 ID",
        },
    )
    tag_strings = fields.List(
        fields.Str(required=True),
        metadata={
            "description": "신설하거나 붙이고자 하는 카테고리 ID",
        },
    )


class StudyGroupReadSchema(Schema):
    """
    스터디그룹의 정보 조회를 위해서 필요한 스키마입니다.
    """

    category_set = fields.Nested(
        CategorySchema(many=True),
        metadata={
            "description": "해당 게시물의 카테고리 정보들",
        },
    )
    leader = fields.Nested(
        AuthorSchema(),
        metadata={
            "description": "해당 스터디의 스터디장 정보",
        },
    )
    start_date = fields.Date(
        metadata={
            "description": "스터디 시작일자",
        },
    )
    end_date = fields.Date(
        metadata={
            "description": "스터디 종료일자",
        },
    )
    user_limit = fields.Int(
        metadata={
            "description": "모집 멤버 수",
        },
    )
    name = fields.Str(
        metadata={
            "description": "개설하고자 하는 스터디의 이름",
            "example": "Make Django GREAT Again. DRF 스터디",
        },
    )


class RecruitmentPostReadSchema(Schema):
    """
    스터디그룹 홍보글 조회를 위해서 필요한 스키마입니다.
    """

    studygroup = fields.Nested(
        StudyGroupReadSchema(),
        metadata={
            "description": "해당 게시물에 맞는 스터디그룹의 정보",
        },
    )
    title = fields.Str(
        required=True,
        metadata={
            "description": "스터디그룹 홍보 게시물의 제목",
            "example": "Django-REST-Framework 스터디를 모집합니다!",
        },
    )
    deadline = fields.Date(
        required=True,
        metadata={
            "description": "스터디 모집 기한",
        },
    )
    content = fields.Str(
        required=True,
        metadata={
            "description": "스터디그룹 홍보 게시물의 내용",
            "example": "DRF 는 Django 사용 시 거의 표준이 되었다고 해도 무방한 프레임워크가 되었습니다.. 같이 스터디 해요!",
        },
    )


class PaginatedRecruitmentPostListSchema(PaginationResponseSchema):
    """
    페이지네이션 된 형태로 스터디 홍보글을 조회하기 위해서 필요한 스키마입니다.
    """

    results = fields.List(
        fields.Nested(RecruitmentPostReadSchema()),
        metadata={"description": "스터디 목록"},
    )
