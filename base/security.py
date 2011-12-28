from functools import wraps
from flask import request
from base import Base

def withPassword(f):
    @wraps(f)
    def checkPassword(*args, **kwargs):
        # Check HTTP Header
        if request.headers.has_key("Authtoken"):
            request.headers.get("Authtoken") == Base.app.config["AUTHPASS"]
            return f(*args, **kwargs)
        # Check GET param
        elif (request.args.has_key('password') and
            request.args.get('password') == Base.app.config["AUTHPASS"]
            ) or (request.form.has_key('password') and
            request.form.get('password') == Base.app.config["AUTHPASS"]):
            return f(*args, **kwargs)
        else:
            return "no access"
    return checkPassword

