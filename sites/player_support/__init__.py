from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from ...constants import APPEAL_LIMIT, MESSAGE_LIMIT, DATA_FILENAME
from ...helpers import load_json, write_json, validate_player_name
from flask_babel import gettext
from datetime import datetime
from ...internals.limiting import limiter

player_support = Blueprint("player_support", __name__, url_prefix="/support")

@player_support.route("/")
def home():
    return render_template("player_support/main.html")

@player_support.route("/appeal", methods = ["GET", "POST"])
@limiter.limit(APPEAL_LIMIT)
def appeal():
    if request.method == "POST":
        data = request.form
        if (not "player" in data.keys()) or (not validate_player_name(data["player"])):
            flash(
                gettext("Invalid player name."), "danger"
            )

            return redirect(
                url_for("player_support.appeal")
            ), 400
        
        _tmp = load_json(DATA_FILENAME)

        if data["player"] in _tmp["admin_responses"].keys() and _tmp["admin_responses"][data["player"]] == "rejected":
            if _tmp["bans"][data["player"]] != "permanent":
                flash(gettext("You did already appeal and you got rejected. You'll have to wait until your ban expires, then you are allowed to play again."), "danger")
            else:
                flash(gettext("Sorry, but your former appeal already got rejected. Therefore, you won't be able to appeal anymore and your ban will stay permanent."), "danger") 
            return redirect(url_for("player_support.appeal")), 403

        if not data["player"] in _tmp["bans"].keys():
            flash(
                gettext("This player has nothing to appeal."), "danger"
            )

            return redirect(
                url_for("player_support.appeal")
            ), 400

        _tmp["appeals"][data["player"]] = data["reason"]
        write_json(_tmp, DATA_FILENAME)

        flash(
            gettext("The appeal has been sent and will soon be processed by an administrator."), "success"
        )

    return render_template("player_support/appeal.html")

@player_support.route("/status", methods = ["GET", "POST"])
def status():
    if request.method == "GET":
        return render_template("player_support/status.html")
    
    player = request.form["player"]
    if (not player) or (not validate_player_name(player)):
        flash(gettext("Invalid input."), "danger")
        return redirect(url_for("player_support.status"))

    status = []
    _tmp = load_json(DATA_FILENAME)
    if player in _tmp["bans"].keys():
        status.append(
            gettext("Player is banned.")
        )
        status.append(
            gettext("Ban expiry: %s") % (datetime.utcfromtimestamp(_tmp["bans"][player]).strftime('%d.%m.%Y %H:%M:%S UTC') if _tmp["bans"][player] != "permanent" else "permanent")
        )

    if player in _tmp["appeals"].keys():
        status.append(
            gettext("Ban appeal sent. Message: %s") % _tmp["appeals"][player]
        )
    if player in _tmp["admin_responses"].keys():
        status.append(
            gettext("Admin response to ban appeal: %s") % _tmp["admin_responses"][player]
        )
    elif player in _tmp["bans"].keys():
        status.append(
            gettext("No admin response to any ban appeals yet.")
        )

    if player in _tmp["warnings"].keys():
        status.append(
            gettext("Player has warning(s): %s warnings given") % _tmp["warnings"][player]
        )

    if status == []:
        status.append(
            gettext("No significant information about this player.")
        )

    return render_template("player_support/status.html", status = status)

@player_support.route("/message", methods = ["GET", "POST"])
@limiter.limit(MESSAGE_LIMIT)
def message():
    if request.method == "GET":
        return render_template("player_support/message.html")

    data = request.form

    if data["message"] and len(data["message"]) < 3000 and len(data["message"]) > 20:
        _tmp = load_json(DATA_FILENAME)
        _tmp["messages"].append(data["message"])
        write_json(_tmp, DATA_FILENAME)

    flash(gettext("We received your message."), "success")

    return render_template("player_support/message.html")