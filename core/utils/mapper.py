from flask_sqlalchemy import Pagination


def sqlalchemy_pagination_mapper(pagination_result: Pagination) -> dict:
    return dict(
        count=pagination_result.total,
        next=pagination_result.next_num,
        previous=pagination_result.prev_num,
        results=pagination_result.items,
    )
