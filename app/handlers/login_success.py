from typing import Awaitable, Optional
import tornado.web
import tornado.ioloop

from app.utils.constants import Key
from app.utils.authentication import Token
from app.utils.common import render_error_page, get_cas_login_page_url, set_cookie


class LoginSuccessHandler(tornado.web.RequestHandler):
    def prepare(self) -> Awaitable[None] | None:

        try:
            token = self.get_argument(Key.TOKEN, None)
            print(f"Received token:{token}")
            if token:
                payload = Token.validate(self, token)
                set_cookie(self, Key.USER_ID, payload)
                set_cookie(self, Key.FULLNAME, payload)
                set_cookie(self, Key.TOKEN, token)

                self.request.payload = payload
            else:
                render_error_page(
                    render_error_page(message="Please try logging in again.", redirect_url=get_cas_login_page_url(self), redirect_text="Login Again")
                )
        except Exception as e:
            str(e)
            render_error_page(redirect_url="/", redirect_text="Go to Homepage")

        return super().prepare()
    
    def get(self):
        host_url = self.get_argument(Key.HOST_URL, "/")
        payload = self.request.payload
        print(f"Login successful for user[{Key.USER_ID}:{payload[Key.USER_ID]}, {Key.FULLNAME}:{payload[Key.FULLNAME]}]")
        self.redirect(host_url)