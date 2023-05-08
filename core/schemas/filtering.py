from marshmallow import Schema, post_load

from core.entities.filtering import FilteringRequest


class BaseFilteringSchema(Schema):
    @post_load
    def to_entity(self, data, **kwargs) -> FilteringRequest:
        return FilteringRequest(**data)
