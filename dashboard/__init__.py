from flask import Blueprint, render_template, request, url_for, flash, redirect
from ..helpers import login_required, load_json, write_json, validate_player_name
from ..constants import DATA_FILENAME
from ..internals.api import execute_kick, execute_ban, send_chat_warning
import time

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")

def add_to_list_of_known_players(player):
    _tmp = load_json(DATA_FILENAME)
    if not player in _tmp["known_players"]:
        _tmp["known_players"].append(player)
        write_json(_tmp, DATA_FILENAME)
        flash("Added player to list of known players.", "success")
    else:
        flash("Player already on list.", "danger")

def remove_from_list_of_known_players(player):
    _tmp = load_json(DATA_FILENAME)
    if player in _tmp["known_players"]:
        _tmp["known_players"].remove(player)
        write_json(_tmp, DATA_FILENAME)
        flash("Removed player from list of known players.", "success")
    else:
        flash("Player not found on list.", "danger")

def add_warning_to_player(player):
    _tmp = load_json(DATA_FILENAME)
    if not player in _tmp["warnings"]:
        _tmp["warnings"][player] = 1
    else:
        _tmp["warnings"][player] += 1
    send_chat_warning(player, _tmp["warnings"][player])

    write_json(_tmp, DATA_FILENAME)
    flash(f"Gave one warning to {player}", "success")

def remove_warning_from_player(player):
    _tmp = load_json(DATA_FILENAME)
    if not player in _tmp["warnings"]:
        flash("The player has no warnings.", "danger")
        return
    else:
        if _tmp["warnings"][player] > 1:
            _tmp["warnings"][player] -= 1
        else:
            del _tmp["warnings"][player]

    write_json(_tmp, DATA_FILENAME)
    flash(f"Removed one warning from {player}", "success")

@dashboard.route("/")
@login_required
def home():
    return render_template("dashboard/home.html")

@dashboard.route("/kick")
@login_required
def kick():
    known = load_json(DATA_FILENAME)["known_players"]
    return render_template("dashboard/kick.html", list_of_players = known)

@dashboard.route("/ban")
@login_required
def ban():
    known = load_json(DATA_FILENAME)["known_players"]
    return render_template("dashboard/ban.html", list_of_players = known)

@dashboard.route("/warnings")
@login_required
def warnings():
    warnings = load_json(DATA_FILENAME)["warnings"]
    return render_template("dashboard/warnings.html", warnings = warnings)

@dashboard.route("/etc")
@login_required
def etc():
    known = load_json(DATA_FILENAME)["known_players"]
    return render_template("dashboard/etc.html", list_of_players = known)

@dashboard.route("/kick/run", methods = ["POST"])
@login_required
def run_kick():
    data = request.form
    if not data["player"]:
        flash("You must provide a player name.", "danger")
        return redirect(
            url_for("dashboard.kick")
        )

    if not validate_player_name(data["player"]):
        flash("Invalid input.", "danger")
        return redirect(
            url_for("dashboard.kick")
        )

    if "remember" in data.keys() and data["remember"] == "on":
        add_to_list_of_known_players(data["player"])

    if "warn" in data.keys() and data["warn"] == "on":
        add_warning_to_player(data["player"])

    execute_kick(data["player"])
    flash("Sent kick signal to server.", "success")

    return redirect(
        url_for("dashboard.kick")
    )

@dashboard.route("/ban/run", methods = ["POST"])
@login_required
def run_ban():
    data = request.form
    if not data["player"]:
        flash("You must provide a player name.", "danger")
        return redirect(
            url_for("dashboard.kick")
        )

    if "remember" in data.keys() and data["remember"] == "on":
        add_to_list_of_known_players(data["player"])

    DIMENSIONS_TRANSLATED = {
        "minutes": 60,
        "hours": 60 * 60,
        "days": 60 * 60 * 24,
        "weeks": 60 * 60 * 24 * 7,
        "months": 60 * 60 * 24 * 31,
        "permanent": -1
    }

    if not data["duration-dimension"] in DIMENSIONS_TRANSLATED.keys():
        flash("Choose a correct dimension.", "danger")
        return redirect(url_for("dashboard.ban"))

    duration_in_seconds = int(data["duration"]) * DIMENSIONS_TRANSLATED[
        data["duration-dimension"]
    ]
    ban_end_timestamp = round(time.time()) + duration_in_seconds
    
    execute_ban(data["player"], (ban_end_timestamp if duration_in_seconds > 0 else "permanent"))
    flash("Player banned for %s %s." % (data["duration"], data["duration-dimension"])
          if data["duration-dimension"] != "permanent" else "Player banned permanently.", "success")
    
    return redirect(
        url_for("dashboard.ban")
    )

@dashboard.route("/list/remove", methods = ["POST"])
@login_required
def remove_from_list():
    data = request.form

    remove_from_list_of_known_players(data["player"])

    return redirect(
        url_for("dashboard.etc")
    )

@dashboard.route("/list/add", methods = ["POST"])
@login_required
def add_to_list():
    data = request.form

    add_to_list_of_known_players(data["player"])

    if "warn" in data.keys() and data["warn"] == "on":
        add_warning_to_player(data["player"])

    return redirect(
        url_for("dashboard.etc")
    )

@dashboard.route("/warnings/add", methods = ["POST"])
@login_required
def add_warn_route():
    data = request.form

    add_warning_to_player(data["player"])

    return redirect(
        url_for("dashboard.warnings")
    )

@dashboard.route("/warnings/remove", methods = ["POST"])
@login_required
def remove_warn_route():
    data = request.form

    remove_warning_from_player(data["player"])

    return redirect(
        url_for("dashboard.warnings")
    )