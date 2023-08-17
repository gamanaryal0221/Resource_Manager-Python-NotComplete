import tornado.web
import tornado.ioloop

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(200)
        self.write("Hello World !")