from core.extensions import ma


class UserSchema(ma.SQLAlchemySchema):
    id = ma.auto_field()
    username = ma.auto_field()
    password = ma.auto_field()
    email = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
