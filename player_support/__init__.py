from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..constants import APPEAL_LIMIT, MESSAGE_LIMIT, DATA_FILENAME
from ..helpers import load_json, write_json, validate_player_name
from flask_babel import gettext

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func = get_remote_address
)

player_support = Blueprint("player_support", __name__, url_prefix="/support")

@player_support.route("/")
def home():
    return render_template("player_support/main.html")

@player_support.route("/appeal", methods = ["GET", "POST"])
@limiter.limit(APPEAL_LIMIT)
def appeal():
    if request.method == "POST":
        data = request.form
        if not validate_player_name(data["player"]):
            flash(
                gettext("Invalid player name."), "danger"
            )

            return redirect(
                url_for("player_support.appeal")
            )
        
        _tmp = load_json(DATA_FILENAME)

        if not data["player"] in _tmp["bans"].keys():
            flash(
                gettext("This player has nothing to appeal."), "danger"
            )

            return redirect(
                url_for("player_support.appeal")
            )

        _tmp["appeals"][data["player"]] = data["reason"]
        write_json(_tmp, DATA_FILENAME)

        flash(
            gettext("The appeal has been sent and will soon be processed by an administrator."), "success"
        )

    return render_template("player_support/appeal.html")

@player_support.route("/status")
def status():
    return render_template("player_support/appeal.html")

@player_support.route("/message")
@limiter.limit(MESSAGE_LIMIT)
def message():
    return render_template("player_support/appeal.html")