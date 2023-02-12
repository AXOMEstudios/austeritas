from flask import Flask

from .auth import auth
from .dashboard import dashboard
from .main import main
from .constants import DEBUG, HAS_HTTPS

from dotenv import load_dotenv
from os import getenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)

    app.config["TEMPLATES_AUTO_RELOAD"]     = DEBUG
    app.config["SECRET_KEY"]                = getenv("SECRET_KEY")
    app.config["SESSION_COOKIE_SECURE"]     = HAS_HTTPS
    app.config["SESSION_COOKIE_HTTPONLY"]   = True
    app.config["SESSION_COOKIE_SAMESITE"]   = "Strict"

    return app