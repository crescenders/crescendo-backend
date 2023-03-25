from flask_restx import fields


class BaseMarshaller:
    @classmethod
    def to_model_dict(cls) -> dict:
        fields_dict = {}
        for attr_name in dir(cls):
            attr_value = getattr(cls, attr_name)
            if isinstance(attr_value, fields.Raw):
                fields_dict[attr_name] = attr_value
        return fields_dict
