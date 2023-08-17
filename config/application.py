import tornado.web

from config.url_mappings import get_urls
from app import settings

def make_app():
    app = tornado.web.Application(
        get_urls(),
        debug=settings.DEBUG
    )

    return app