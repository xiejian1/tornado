# -*- coding: utf-8 -*-
#用于规定字符编码，想要中文正常最好就加上这句

import os.path
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from view.Handler import *
#巴拉巴拉import一大堆tornado的东西，反正都有用，原封不动即可

import pymongo
#这里是导入MongoDB

define("port", default=8002, help="run on the given port", type=int)
#定义监听的端口，随便挑个喜欢的数字吧

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/edit/([0-9Xx\-]+)", EditHandler),
            (r"/add", EditHandler),
            (r"/delete/([0-9Xx\-]+)", DelHandler),
            (r"/blog/([0-9Xx\-]+)", BlogHandler),
            (r"/hello",HelloHandler)
        ]
        settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        conn = pymongo.MongoClient(host="localhost",port=27017)
        self.db = conn["demo"]
        tornado.web.Application.__init__(self, handlers=handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()