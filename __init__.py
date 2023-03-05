from flask import Flask

from .auth import auth
from .dashboard import dashboard
from .main import main
from .player_support import player_support
from .constants import DEBUG, HAS_HTTPS, LANGUAGE, MAX_CONTENT_SIZE

from .internals.clock import init_clock
from dotenv import load_dotenv
from os import getenv
from flask_babel import Babel

load_dotenv()
init_clock()

def create_app(testing = False):
    app = Flask(__name__)
    babel = Babel(app, locale_selector = lambda: LANGUAGE)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(player_support)

    app.config["TESTING"]                   = testing
    app.config["TEMPLATES_AUTO_RELOAD"]     = DEBUG
    app.config["SECRET_KEY"]                = getenv("SECRET_KEY")
    app.config["SESSION_COOKIE_SECURE"]     = HAS_HTTPS
    app.config["SESSION_COOKIE_HTTPONLY"]   = True
    app.config["SESSION_COOKIE_SAMESITE"]   = "Strict"
    app.config["BABEL_DEFAULT_LOCALE"]      = "en"
    app.config["MAX_CONTENT_LENGTH"]        = MAX_CONTENT_SIZE

    return app