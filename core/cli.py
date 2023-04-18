import click
from flask.cli import with_appcontext


@click.command("init-app")
@with_appcontext
def init_app():
    """애플리케이션을 시작합니다."""


@click.command("createadminuser")
@with_appcontext
def createadminuser():
    """사용자를 생성합니다."""
    from core.entities.pagination import PaginationEntity
    from crescendo.auth.entities import UserEntity
    from crescendo.auth.models import UserModel
    from crescendo.auth.repositories import SQLAlchemyUserRepository

    email = click.prompt("email:", type=str)
    username = click.prompt("username", type=str)

    superuser = UserEntity(email=email, username=username, role="ADMIN")

    SQLAlchemyUserRepository(
        user_entity_cls=UserEntity,
        user_model_cls=UserModel,
        pagination_entity_cls=PaginationEntity,
    ).save(user_entity=superuser)
