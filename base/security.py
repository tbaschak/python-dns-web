from functools import wraps
from flask import request
from base import app

def withPassword(f):
    @wraps(f)
    def checkPassword(*args, **kwargs):
        # Check HTTP Header
        print request.headers.keys()
        if request.headers.has_key("Authtoken"):
            request.headers.get("Authtoken") == app.config["AUTHPASS"]
            return f(*args, **kwargs)
        # Check GET param
        elif (request.args.has_key('password') and
            request.args.get('password') == app.config["AUTHPASS"]
            ) or (request.form.has_key('password') and
            request.form.get('password') == app.config["AUTHPASS"]):
            return f(*args, **kwargs)
        else:
            return "no access"
    return checkPassword

