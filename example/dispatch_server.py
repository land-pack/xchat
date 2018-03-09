import ujson
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from collections import defaultdict

name_users = dict()

class PlayManager(object):
    name2connection =  dict()

    @classmethod
    def join(cls, name, conn):
        cls.name2connection[name] = conn

    @classmethod
    def leave(cls, name):
        del cls.name2connection[name]

    @classmethod
    def pub(cls, msg, white_list=[], black_list=[]):

        mix_list = set(cls.name2connection.keys()) - set(black_list)
        player_list = white_list if white_list else list(mix_list)

        for name in player_list:
            try:
                conn = cls.name2connection.get(name)
                conn.write_message(msg)
            except:
                print("Can not found any play name as {} and connect db current {}".format(name, conn))
    

    @classmethod
    def dispatch(cls, data):
        receivers = data.get("receivers")
        msg = data.get("msg")
        cls.pub(msg, white_list=receivers)
        

    @classmethod
    def member(cls):
        return ujson.dumps(cls.name2connection.keys())
        


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    
    def prepare(self):
        d = {k:v[0] for k, v in self.request.arguments.iteritems()}
        self.arg = d
        print('websocket arguments:%s', d)

    def check_origin(self, origin):
        return True

    def open(self):
        name = self.arg.get("name")
        print("Open Connection by  {}".format(name))
        #name_users[name]= self

        # New player join, publish a join message
        data = {
            "tid": "join",
            "name": name
        }
        data_str = ujson.dumps(data)
        PlayManager.pub(data_str)
        PlayManager.join(name, self)
        
        PlayManager.pub(PlayManager.member(), black_list=name)


    def on_message(self, message):
        # self.write_message("Your message was: " + message)
        # who you want to talk
        try:
            data = ujson.loads(message)
        except:
            self.write_message("Unable to parser your data structure")
        else:
            PlayManager.dispatch(data)



    def on_close(self):
        #del name_users[self.arg.name]
        print("Close Connection")

        # user leave
        PlayManager.leave(self.arg.get("name"))
        data = {
            "tid": "leave",
            "name": self.arg.get("name")
        }
        data_str = ujson.dumps(data)
        PlayManager.pub(data_str)

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
