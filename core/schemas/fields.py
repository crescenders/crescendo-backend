import re
import typing

from marshmallow import fields, utils


class SortDict(fields.Field):
    """Overrides the field to make it easier to parse `fieldname:sortinformation` in the URL."""

    default_error_messages = {"invalid": "Not a valid SortDict."}

    def _deserialize(
        self,
        value: typing.Any,
        attr: str | None,
        data: typing.Mapping[str, typing.Any] | None,
        **kwargs,
    ):
        if not isinstance(value, (str, bytes)):
            raise self.make_error("invalid")
        try:
            value = utils.ensure_text_type(value)
            # validate the value, make sure it's a valid sort information.
            regex = re.compile(r"^(\w+):(asc|desc)$")
            if not regex.search(value):
                raise self.make_error("invalid")
            # split the value into the field name and the sorting direction.
            sorting_field = value.split(":")[0]
            sorting_direction = value.split(":")[1]
            return {sorting_field: sorting_direction}
        except UnicodeDecodeError as error:
            raise self.make_error("invalid_utf8") from error
