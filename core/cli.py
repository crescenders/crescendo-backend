import click
from flask.cli import with_appcontext


@click.command("init-app")
@with_appcontext
def init_app():
    """애플리케이션을 시작합니다."""
