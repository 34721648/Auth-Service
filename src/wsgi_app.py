from gevent import monkey
from gevent.pywsgi import WSGIServer

from app import app
from settings import settings

monkey.patch_all()


http_server = WSGIServer(('', settings.wsgi.port), app)
http_server.serve_forever()
