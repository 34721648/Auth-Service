from gevent import monkey

monkey.patch_all()

from typing import Optional

import typer
from gevent.pywsgi import WSGIServer

from api.v1.account import account_service
from app import app
from services.exceptions import UserAlreadyExists
from settings import settings

typer_app = typer.Typer()


@typer_app.command()
def runserver():
    http_server = WSGIServer(  # noqa: WPS317
        (
            settings.wsgi.host,
            settings.wsgi.port,
        ),
        application=app,
        spawn=settings.wsgi.workers,
    )
    http_server.serve_forever()


@typer_app.command()
def create_superuser(
    login: str,
    password: str,
    email: Optional[str] = None,
) -> None:
    email = email or f'{login}@mail.ru'
    try:
        account_service.create_user(
            login=login,
            password=password,
            email=email,
            is_superuser=True,
        )
    except UserAlreadyExists:
        print(  # noqa: WPS421
            f'Failed to create superuser! User with login {login} already exists.',
        )
    print(f'User {login} created!')  # noqa: WPS421


if __name__ == '__main__':
    typer_app()
