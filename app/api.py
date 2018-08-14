# pytokens
# create by gnomezworc
#
#!/usr/bin/python3

from wsgiref.simple_server import make_server
from pycnic.core import WSGI, Handler

class Home(Handler):
    def get(self):
        return {"message":"hello"}

class app(WSGI):
    routes = [
        ('/', Home())
    ]

try:
    print("Serving on 0.0.0.0:8080...")
    make_server('0.0.0.0', 8080, app).serve_forever()
except KeyboardInterrupt:
    pass
print("\nServeur Stop")
