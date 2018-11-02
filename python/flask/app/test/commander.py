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
        return "Hello World!"


def init_route(route_list):
    for route in route_list:
        api.add_resource(*route)


def main():
    route_list = [(Hello,'/hello')]
    init_route(route_list)
    app.run()

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)

    # http_server.bind(8080)
    http_server.start(4)

    IOLoop.instance().start()

if __name__ == '__main__':
    main()
