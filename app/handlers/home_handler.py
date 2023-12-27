from typing import Awaitable, Optional
import tornado.web
import tornado.ioloop

from app.utils.authentication import JwtToken

from app.utils.constants import Template

class HomeHandler(tornado.web.RequestHandler):
    def prepare(self) -> Awaitable[None] | None:
        self.request.payLoad = JwtToken.validate(self)
        return super().prepare()

    def get(self):

        self.render(Template.HOME)