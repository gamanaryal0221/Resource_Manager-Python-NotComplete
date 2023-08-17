import tornado.web
import re

from app import settings

from app.handlers.home_handler import HomeHandler

def get_urls():
    print('\n---------- Initializing url -> handlers ----------')

    handlers = [
        (fr"/", HomeHandler),
        (fr"{settings.STATIC_URL}", tornado.web.StaticFileHandler, {"path": settings.STATIC_PATH}),
    ]

    for i, handler in enumerate(handlers):
        print(f'{i+1}. {handler[0]} -> {get_handler_name(handler[1])}')

    return handlers

def get_handler_name(_class):
    class_name = re.search(r"'(.*?)'", str(_class)).group(1)
    return str(class_name)
