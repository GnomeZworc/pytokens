# pytokens
# create by gnomezworc
#
#!/usr/bin/python3

from pycnic.errors import HTTP_401
from functools import wraps
from variables import env

def check_head_token(request):
    token = request.get_header("token")
    if token and token == env("TOKEN"):
        return True
    return False

def require(database):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            database.logs("connect in " + args[0].request.path + " from " + args[0].request.ip)
            if check_head_token(args[0].request) == False:
                database.logs("try to connect from " + args[0].request.ip + " with bad token")
                raise HTTP_401("bad token")
            return f(*args, **kwargs)
        return wrapped
    return wrapper
