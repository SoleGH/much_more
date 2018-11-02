from flask import Flask
from flask_restful import Api
from flask_restful import Resource
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer


app = Flask(__name__)
api = Api(app)


class Hello(Resource):
    @staticmethod
    def get():
        return "Hello flask tornado!"


def init_route(route_list):
    for route in route_list:
        api.add_resource(*route)


def main():
    route_list = [(Hello,'/hello')]
    init_route(route_list)

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)

    # 开启多线程,但start需要调用os.fork()函数,windows下os没有该函数
    # http_server.bind(5000)
    # http_server.start(0)

    IOLoop.instance().start()
"""
单进程:
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.instance().start()

+++++++++++++++++++++++++++++
多进程
http_server = HTTPServer(WSGIContainer(app))
# 开启多线程,但start需要调用os.fork()函数,windows下os没有该函数
# http_server.bind(5000)
# http_server.start(0)  # 指定fork子进程数量

IOLoop.instance().start()

+++++++++++++++++++++++++++++
高级多进程
sockets = tornado.netutil.bind_sockets(8888)
tornado.process.fork_processes(0)
server = HTTPServer(app)
server.add_sockets(sockets)
IOLoop.current().start()
"""

if __name__ == '__main__':
    main()
