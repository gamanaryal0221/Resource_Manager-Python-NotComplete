from typing import Awaitable, Optional
import tornado.web
import tornado.ioloop

from app.utils.authentication import Token

from app.utils.constants import Template
from app.utils.authentication import Password

class HomeHandler(tornado.web.RequestHandler):
    def prepare(self) -> Awaitable[None] | None:
        self.request.payLoad = Token.validate(self)
        return super().prepare()

    def get(self):

        self.render(Template.HOME)