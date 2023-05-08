from flask_marshmallow import Schema  # type: ignore[import]
from marshmallow import post_load

from core.entities.sorting import SortingRequest
from core.schemas import fields


class SortingRequestSchema(Schema):
    sort_by = fields.Sorting(
        metadata={"description": "정렬 조건입니다. `필드명:정렬조건(asc or desc)` 형식을 준수해야 합니다."}
    )

    @post_load
    def to_entity(self, data, **kwargs) -> SortingRequest:
        return SortingRequest(**data)
