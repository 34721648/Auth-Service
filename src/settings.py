from datetime import timedelta

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


def build_dsn(
    protocol: str,
    user: str,
    password: str,
    host: str,
    port: int,
    path: str,
) -> str:
    return f'{protocol}://{user}:{password}@{host}:{port}/{path}'


class DatabaseSettings(BaseSettings):
    protocol: str = 'postgresql'
    user: str = 'postgres'
    password: str = '123'
    host: str = 'localhost'
    port: int = 5432
    name: str = 'auth_database'

    @property
    def dsn(self) -> str:
        return build_dsn(
            protocol=self.protocol,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        )

    class Config:
        env_prefix = 'AUTH_DB_'


class RedisSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 6379

    class Config:
        env_prefix = 'AUTH_REDIS_'


class JWTSettings(BaseSettings):
    access_token_expire_time: timedelta = timedelta(minutes=1)
    refresh_token_expire_time: timedelta = timedelta(days=7)
    token_location: list[str] = ['headers']
    secret_key: str = 'DEBUG'


class WSGISettings(BaseSettings):
    """
    Config for running the app. Not used in main app config.
    """

    host: str = "0.0.0.0"
    port: int = 5001
    workers: int = 3

    class Config:
        env_prefix = "AUTH_WSGI_"


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    jwt: JWTSettings = JWTSettings()
    wsgi: WSGISettings = WSGISettings()


settings = Settings()