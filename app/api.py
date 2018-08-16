# pytokens
# create by gnomezworc
#
#!/usr/bin/python3

from wsgiref.simple_server import make_server
from pycnic.core import WSGI, Handler
from functools import wraps
from variables import env
from database import mongo
from require import require

Database = mongo(host=env("MONGO_HOST"), port=env("MONGO_PORT"), database=env("MONGO_DATABASE"), protocol=env("MONGO_PROTOCOL"), api=env("API_NAME"))

class Home(Handler):
    @require(Database)
    def get(self):
        return {"message":"hello"}

class app(WSGI):
    routes = [
        ('/', Home())
    ]

try:
    print("Serving on " + env("HOST") + ":" + env("PORT") + "...")
    make_server(env("HOST"), int(env("PORT")), app).serve_forever()
except KeyboardInterrupt:
    pass
Database.close()
print("\nServeur Stop")
