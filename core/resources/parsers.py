from flask_restx import reqparse


def get_list_parser(parser: reqparse.RequestParser) -> reqparse.RequestParser:
    """리스트 리소스에 대한 기본 파서를 정의합니다.
    페이지네이션 정보, 검색어 정보가 포함됩니다."""
    parser.add_argument(
        "size", type=int, required=False, location="args", help="페이지의 크기"
    )
    parser.add_argument(
        "page", type=int, required=False, location="args", help="페이지의 숫자"
    )
    parser.add_argument("query", type=str, required=False, location="args", help="검색어")
    return parser
