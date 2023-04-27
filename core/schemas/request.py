from marshmallow import Schema, fields
from marshmallow.validate import OneOf, Range


class PaginateArgsSchema(Schema):
    """
    페이지네이션을 위해 사용되는 파라미터입니다.

    page 의 기본값은 1, per_page 의 기본값은 10 입니다.
    """

    page = fields.Integer(
        load_default=1,
        validate=Range(min=1),
        metadata={"description": "페이지"},
    )
    per_page = fields.Integer(
        load_default=10,
        validate=Range(min=1),
        metadata={"description": "페이지당 보여줄 아이템 개수"},
    )


class FilteringArgsSchema(Schema):
    """검색 조건을 위해 사용되는 파라미터입니다."""

    filter_by = fields.String(load_default=None, metadata={"description": "검색어"})


class OrderingArgsSchema(Schema):
    """
    정렬 조건을 위해 사용되는 파라미터입니다.

    "desc", "asc" 두 개의 값만 받을 수 있습니다.
    """

    ordering = fields.String(
        load_default="desc",
        validate=OneOf(["desc", "asc"]),
        metadata={
            "description": "정렬 조건",
        },
    )
