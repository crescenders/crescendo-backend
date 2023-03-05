from core.extensions import ma
from crescenders.users.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class UserListReadSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    uuid = ma.auto_field()
    email = ma.auto_field()
    username = ma.auto_field()
    full_name = ma.Method("get_full_name")

    def get_full_name(self, obj):
        return obj.get_full_name()
