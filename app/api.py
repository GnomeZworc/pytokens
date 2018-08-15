# pytokens
# create by gnomezworc
#
#!/usr/bin/python3

from wsgiref.simple_server import make_server
from pycnic.core import WSGI, Handler
from variables import env

class Home(Handler):
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
print("\nServeur Stop")
