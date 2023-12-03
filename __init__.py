from os import getenv

from dotenv import load_dotenv
from flask import Flask
from flask_babel import Babel
from waitress import serve

from src.constants import DEBUG, HAS_HTTPS, LANGUAGE, MAX_CONTENT_SIZE
from src.internals.clock import init_clock
from src.internals.limiting import limiter
from src.sites.auth import auth
from src.sites.dashboard import dashboard
from src.sites.main import main
from src.sites.player_support import player_support
from src.sites.chat_checking import chat_checking


def create_app(testing=False):
    app = Flask(__name__)

    babel = Babel(app, locale_selector=lambda: LANGUAGE)

    load_dotenv()
    init_clock(testing)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(player_support)
    app.register_blueprint(chat_checking)

    limiter.init_app(app)

    app.config["TESTING"] = testing
    app.config["TEMPLATES_AUTO_RELOAD"] = DEBUG
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["SESSION_COOKIE_SECURE"] = HAS_HTTPS
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
    app.config["BABEL_DEFAULT_LOCALE"] = "en"
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_SIZE

    app.template_folder = "src/templates"
    app.static_folder = "src/static"

    return app


if __name__ == "__main__":
    serve(create_app(), port=8000, threads=1)
