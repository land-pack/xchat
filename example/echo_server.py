import tornado.websocket
import tornado.httpserver
import tornado.ioloop

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    
    def check_origin(self, origin):
        return True

    def open(self):
        print("Open Connection")

    def on_message(self, message):
        self.write_message("Your message was: " + message)

    def on_close(self):
        print("Close Connection")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/ws', WebSocketHandler),
        ]
        tornado.web.Application.__init__(self, handlers)


if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(9001)
    tornado.ioloop.IOLoop.instance().start()
