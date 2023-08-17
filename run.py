import tornado.web
import tornado.ioloop

from config.application import make_app
from app import settings

if __name__ == "__main__":
    print('\n--------------------- Starting application ---------------------')
    app = make_app()

    port  = settings.PORT
    app.listen(port)

    # Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    # C:\Apache24\bin\httpd.exe
    # /user/(?P<action>create|list|profile|edit|delete)
    print(f"\nServer is live on http://localhost:{port}")
    tornado.ioloop.IOLoop.instance().start()