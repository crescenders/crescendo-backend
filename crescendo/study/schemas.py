from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True)
    description = fields.Str(required=True)


class CategoryCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)


class StudyGroupCreateSchema(Schema):
    """
    스터디그룹과 스터디그룹 홍보 게시물을 작성하기 위해서 필요한 스키마입니다.
    """

    name = fields.Str(required=True)
    user_limit = fields.Int(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    deadline = fields.Date(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    category_id = fields.Int(required=True)


class StudyGroupReadSchema(Schema):
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    title = fields.Str(required=True)
    deadline = fields.Date(required=True)
    content = fields.Str(required=True)
