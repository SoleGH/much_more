from flask import Flask
from flask_restful import Api
from flask_restful import Resource
from gevent.wsgi import WSGIServer


app = Flask(__name__)


@app.route("/hello")
def hello():
    return "hello world"


def main():
    # default port 5000
    app.run()

if __name__ == '__main__':
    main()
