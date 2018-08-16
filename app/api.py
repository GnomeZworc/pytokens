# pytokens
# create by gnomezworc
#
#!/usr/bin/python3

import datetime

from wsgiref.simple_server import make_server
from pycnic.core import WSGI, Handler
from pycnic.errors import HTTP_401
from functools import wraps
from variables import env
from pymongo import MongoClient


class mongo():
    connect = None
    db = None

    def __init__(self, host='127.0.0.1', port='80', database='database', protocol='mongodb'):
        self.connect = MongoClient(protocol + "://" + host + ":" + port + "/")
        self.db = self.connect[database]
        self.logs("api start")
    def close(self):
        self.connect.close()
        self.logs("api stop")
    def logs(self, message):
        elem = {}
        elem["timestamp"] = datetime.datetime.now()
        elem["message"] = message
        self.db["api_tokens_logs"].insert_one(elem)

Database = None

def check_head_token(request):
    token = request.get_header("token")
    if token and token == env("TOKEN"):
        return True
    return False

def require():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            Database.logs("connect in " + args[0].request.path + " from " + args[0].request.ip)
            if check_head_token(args[0].request) == False:
                Database.logs("try to connect from " + args[0].request.ip + " with bad token")
                raise HTTP_401("bad token")
            return f(*args, **kwargs)
        return wrapped
    return wrapper

class Home(Handler):
    @require()
    def get(self):
        return {"message":"hello"}

class app(WSGI):
    routes = [
        ('/', Home())
    ]

try:
    print("Serving on " + env("HOST") + ":" + env("PORT") + "...")
    Database = mongo(host=env("MONGO_HOST"), port=env("MONGO_PORT"), database=env("MONGO_DATABASE"), protocol=env("MONGO_PROTOCOL"))
    make_server(env("HOST"), int(env("PORT")), app).serve_forever()
except KeyboardInterrupt:
    pass
Database.close()
print("\nServeur Stop")
