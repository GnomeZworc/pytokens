# pytokens
# create by gnomezworc
#
#!/usr/bin/python3

import string, random

from wsgiref.simple_server import make_server
from pycnic.core import WSGI, Handler
from pycnic.errors import HTTP_400
from functools import wraps
from variables import env
from database import mongo
from require import require

Database = mongo(host=env("MONGO_HOST"), port=env("MONGO_PORT"), database=env("MONGO_DATABASE"), protocol=env("MONGO_PROTOCOL"), api=env("API_NAME"))

class Home(Handler):
    @require(Database)
    def get(self):
        return {"message":"hello"}

def generate_token(size=64, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

class CreatToken(Handler):
    @require(Database)
    def post(self):
        source = self.request.data.get("source")
        source_id = self.request.data.get("id")
        limit_time = self.request.data.get("limit_time")
        if source == None or source_id == None or limit_time == None:
            raise HTTP_400("we need source, id and limit_time (0 = unlimited)")
        ret = Database.findOne("tokens", {"source_id":source_id})
        if ret != None:
            return {"message":"token already existe for this user", "token":str(ret["token"])}
        token = generate_token()
        while Database.findOne("tokens", {"token":token}) != None:
            token = generate_token()
        elem = {
            "token":token,
            "source":source,
            "source_id":source_id
        }
        Database.insert("tokens", elem)
        return {"message":"new token is create", "token":str(token)}

class CheckToken(Handler):
    @require(Database)
    def post(self):
        source = self.request.data.get("source")
        token = self.request.data.get("token")
        if source == None or token == None:
            raise HTTP_400("we need source and token")
        message = "this token is "
        ret = Database.findOne("tokens", {"source":source,"token":token})
        retour = {}
        if ret != None:
            message += "valid"
            retour["is_valid"] = 1
            retour["id"] = ret["source_id"]
        else:
            message += "not valid"
            retour["is_valid"] = 0
        retour["message"] = message
        return retour


class app(WSGI):
    routes = [
        ('/', Home()),
        ('/create', CreatToken()),
        ('/check', CheckToken())
    ]

try:
    print("Serving on " + env("HOST") + ":" + env("PORT") + "...")
    make_server(env("HOST"), int(env("PORT")), app).serve_forever()
except KeyboardInterrupt:
    pass
Database.close()
print("\nServeur Stop")
