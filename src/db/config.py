from contextlib import contextmanager

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from db.token_storage.redis_storage import RedisTokenStorage
from settings import settings

metadata = MetaData(schema='content')

db = SQLAlchemy()
migrate = Migrate()

token_storage = RedisTokenStorage(redis_host=settings.redis.host, redis_port=settings.redis.port)


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.db.dsn
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)


@contextmanager
def db_session(db: SQLAlchemy):
    try:  # noqa: WPS229
        yield db.session
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
