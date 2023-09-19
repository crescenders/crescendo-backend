from rest_framework.pagination import PageNumberPagination


class StudyGroupPagination(PageNumberPagination):
    page_query_description = "페이지 번호입니다. 기본값은 1입니다."
    page_size = 10
    page_size_query_param = "page_size"
    page_size_query_description = "페이지당 보여줄 스터디그룹의 갯수입니다. 기본값은 6입니다."
