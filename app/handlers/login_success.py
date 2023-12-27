from typing import Awaitable, Optional
import tornado.web
import tornado.ioloop
import traceback

from app.utils.constants import Key
from app.utils.authentication import JwtToken
from app.utils.common import render_error_page, get_cas_login_page_url, refresh_all_cookies


class LoginSuccessHandler(tornado.web.RequestHandler):
    def prepare(self) -> Awaitable[None] | None:

        try:
            token = self.get_argument(Key.TOKEN, None)
            print(f"Received token:{token}")
            if token:
                payload = JwtToken.validate(self, token)
                payload[Key.TOKEN] = token

                if refresh_all_cookies(self, payload):
                    self.request.payload = payload
                else:
                    raise Exception("Could not set cookies")

            else:
                raise Exception("Null token received")

        except:
            traceback.print_exc()
            render_error_page(
                self, message="Please try logging in again.",
                redirect_url=get_cas_login_page_url(self), redirect_text="Login Again"
                )

        return super().prepare()
    
    def get(self):
        host_url = self.get_argument(Key.HOST_URL, "/")
        payload = self.request.payload
        print(f"Login successful for user[{Key.USER_ID}:{payload[Key.USER_ID]}, {Key.FULLNAME}:{payload[Key.FULLNAME]}]")
        self.redirect(host_url)