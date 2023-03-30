from core.resources.marshaller.base_marshaller import BaseMarshaller
from flask_restx import fields


class PaginationMarshaller(BaseMarshaller):
    total = fields.Integer(description="모든 아이템의 개수", example=100)
    page = fields.Integer(description="현재 페이지 번호", example=1)
    per_page = fields.Integer(description="페이지 당 아이템의 개수", example=20)
    pages = fields.Integer(description="전체 페이지의 수", example=5)
