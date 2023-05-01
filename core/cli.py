import click
from flask import cli


@click.command("init-app")
@cli.with_appcontext
def init_app():
    """애플리케이션을 시작합니다."""


@click.command("createadminuser")
@cli.with_appcontext
def createadminuser():
    """사용자를 생성합니다."""
    from core.extensions import db
    from crescendo.auth.models import UserModel

    email = click.prompt("email:", type=str)
    username = click.prompt("username", type=str)

    superuser = UserModel(email=email, username=username, role="ADMIN")
    db.session.add(superuser)
    db.session.commit()
    print(superuser, "is created...")
