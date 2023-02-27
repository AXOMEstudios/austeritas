from functools import wraps
from flask import g, redirect
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from dotenv import load_dotenv
from os import getenv
from json import dump, load
from .constants import CONFIG_FILENAME
from string import ascii_letters, digits

load_dotenv()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            return redirect("/auth/login")
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

def write_json(json, filename=CONFIG_FILENAME):
    with open(filename, "w") as f:
        dump(json, f, indent = 4)
        return json

def load_json(filename=CONFIG_FILENAME):
    with open(filename, "r") as f:
        return load(f)

def validate_player_name(name):
    VALID_SYMBOLS = list(ascii_letters + digits + " " + "_")

    if len(name) > 15 and len(name) < 3:
        return False

    for letter in list(name):
        if not letter in VALID_SYMBOLS:
            return False
    
    return True