# pytokens
# create by gnomezworc
#
#!/usr/bin/python3

from wsgiref.simple_server import make_server
from pycnic.core import WSGI, Handler
from pycnic.errors import HTTP_401
from functools import wraps
from variables import env

def check_head_token(request):
    token = request.get_header("token")
    if token and token == env("TOKEN"):
        return True
    return False

def require():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if check_head_token(args[0].request) == False:
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
    make_server(env("HOST"), int(env("PORT")), app).serve_forever()
except KeyboardInterrupt:
    pass
print("\nServeur Stop")
