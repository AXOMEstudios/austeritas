from functools import wraps
from flask import g, redirect
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            return redirect("/auth/")
        return f(*args, **kwargs)
    return decorated_function

def generate_csrf_token(user, action, expires=600):
    s = Serializer(getenv("SECRET_KEY"), expires)
    return s.dumps({
        "user": str(user),
        "action": action
    }).decode("utf-8")

def validate_csrf_token(token, session_token, action):
    try:
        if session_token["token_" + action] != token:
            return False
    except KeyError:
        return False

    s = Serializer(getenv("SECRET_KEY"))
    try:
        data = s.loads(token.encode("utf-8"))
    except:
        return False
    
    if data["user"] != str(session_token["user"]) or data["action"] != action:
        return False

    return True