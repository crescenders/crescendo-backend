from marshmallow import Schema, fields
from marshmallow.validate import Range


class PaginateArgsSchema(Schema):
    """페이지네이션 요청을 위해 사용되는 파라미터 스키마입니다."""

    page = fields.Integer(
        validate=Range(min=1),
        metadata={
            "description": "조회하고자 하는 페이지 번호입니다." "아무런 값이 전달되지 않을 경우, 기본값은 1 입니다."
        },
    )
    per_page = fields.Integer(
        validate=Range(min=1),
        metadata={"description": "한 페이지의 아이템 개수입니다." "아무런 값이 전달되지 않을 경우, 기본값은 10 입니다."},
    )


class PaginationResultSchema(Schema):
    """페이지네이션 응답을 위해 사용되는 스키마입니다."""

    count = fields.Integer(metadata={"description": "전체 아이템 개수"})
    next_page = fields.URL(metadata={"description": "다음 페이지 URL"})
    previous_page = fields.URL(metadata={"description": "이전 페이지 URL"})
