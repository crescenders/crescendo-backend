from marshmallow import fields, validate
from marshmallow.validate import Range


class PaginateArgsSchemaMixin:
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


class FilteringArgsSchemaMixin:
    filter_by = fields.String(load_default=None, metadata={"description": "검색어"})


class OrderingArgsSchemaMixin:
    ordering = fields.String(
        load_default="desc",
        metadata={
            "description": "정렬 조건",
            "load_validate": validate.OneOf(["asc", "desc"]),
        },
    )
