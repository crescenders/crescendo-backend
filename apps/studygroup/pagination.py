from rest_framework.pagination import CursorPagination


class StudyGroupPagination(CursorPagination):
    page_size = 8
    cursor_query_param = "cursor"
    cursor_query_description = "커서 값입니다."
    invalid_cursor_message = "잘못된 커서 값입니다."
    ordering = "-created_at"


class StudyGroupAssignmentPagination(CursorPagination):
    page_size = 5
    cursor_query_param = "cursor"
    cursor_query_description = "커서 값입니다."
    invalid_cursor_message = "잘못된 커서 값입니다."
    ordering = "-created_at"
