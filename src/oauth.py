from authlib.integrations.flask_client import OAuth

from settings import settings

oauth = OAuth()

oauth.register(
    name=settings.google_auth.name,
    server_metadata_url=settings.google_auth.server_metadata_url,
    client_id=settings.google_auth.client_id,
    client_secret=settings.google_auth.client_secret,
    client_kwargs={
        'scope': 'openid email profile',
    },
)
