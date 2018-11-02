from flask import Flask
from flask_restful import Api
from flask_restful import Resource
from gevent.wsgi import WSGIServer


app = Flask(__name__)
api = Api(app)


class Hello(Resource):
    @staticmethod
    def get():
        return "Hello flask gevent!"


def init_route(route_list):
    for route in route_list:
        api.add_resource(*route)


def main():
    route_list = [(Hello,'/hello')]
    init_route(route_list)
    
    http_server = WSGIServer(('0.0.0.0', int(5000)),app)
    http_server.serve_forever()

if __name__ == '__main__':
    main()
