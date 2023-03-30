from typing import Dict, List, Optional

from flask_restx import Model, fields


class BaseMarshaller:
    def to_model(
        self, model_name: str, field_names: Optional[List[str]] = None
    ) -> dict[str, str | Model]:
        fields_dict = {}
        for attr_name in dir(self):
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, fields.Raw):
                if field_names is None or attr_name in field_names:
                    fields_dict[attr_name] = attr_value
        return {"model": Model(model_name, fields_dict), "name": model_name}
