import re
import time
from base64 import b64encode

from flask import Blueprint, abort, request

from ...constants import CONFIG_FILENAME, DATA_FILENAME
from ...helpers import load_json
from ...internals.api import execute_ban
from ...sites.dashboard import DIMENSIONS_TRANSLATED
from .config import API_KEY

chat_checking = Blueprint("chat_checking", __name__, url_prefix="/v1")


def normalize(text):
    text = text.casefold().replace("ä", "ae").replace("ö", "oe") \
        .replace("ü", "ue").replace("ß", "ss")
    
    return text


blocklist = [normalize(s) for s in load_json(
    "austeritas_config.json")["blocklist"]]


@chat_checking.before_request
def check_api_key():
    if request.headers.get("Authorization") != "Basic " + b64encode(API_KEY.encode()).decode("utf-8"):
        abort(401)


@chat_checking.route("/join", methods=["POST"])
@chat_checking.route("/leave", methods=["POST"])
def check_join_message():
    json_ = request.get_json()
    vanished = load_json(DATA_FILENAME)["vanished"]

    return {
        "response": (json_["player_display_name"] not in vanished),
        "hashed": "",
        "hashes": []
    }


@chat_checking.route("/chat", methods=["POST"])
def check_message():
    json_ = request.get_json()
    player = json_["player_display_name"]
    text = json_["text"]

    allow_message = True

    words = re.split('\W+', text)

    for word in words:
        if normalize(word) in blocklist:
            allow_message = False
            break

    for word in blocklist:
        if word in normalize(text):
            allow_message = False
            break

    if not allow_message:
        autoban_settings = load_json(CONFIG_FILENAME)["autoban_settings"]
        duration_in_seconds = int(autoban_settings["duration"]) * DIMENSIONS_TRANSLATED[
            autoban_settings["duration-dimension"]
        ]
        ban_end_timestamp = round(time.time()) + duration_in_seconds

        execute_ban(
            player, (ban_end_timestamp if duration_in_seconds > 0 else "permanent"))

    return {
        "response": allow_message,
        "hashed": "",
        "hashes": []
    }
