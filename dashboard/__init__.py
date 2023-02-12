from flask import Blueprint, render_template, request, url_for, flash, redirect
from ..helpers import login_required, load_json, write_json, validate_player_name
from ..constants import DATA_FILENAME
from ..internals.api import execute_kick

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")

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
    return render_template("dashboard/etc.html")

@dashboard.route("/kick/run", methods = ["POST"])
@login_required
def run_kick():
    data = request.form

    if "remember" in data.keys() and data["remember"] == "on":
        _tmp = load_json(DATA_FILENAME)
        if not data["player"] in _tmp["known_players"]:
            _tmp["known_players"].append(data["player"])
            write_json(_tmp, DATA_FILENAME)
            flash("Added player to list of known players.", "success")

    if "warn" in data.keys() and data["warn"] == "on":
        _tmp = load_json(DATA_FILENAME)
        if not data["player"] in _tmp["warnings"]:
            _tmp["warnings"][data["player"]] = 1
        else:
            _tmp["warnings"][data["player"]] += 1

        write_json(_tmp, DATA_FILENAME)
        flash(f"Gave one warning to {data['player']}", "success")

    if validate_player_name(data["player"]):
        execute_kick(data["player"])
        flash("Sent kick signal to server.", "success")
    else:
        flash("Invalid input.", "danger")
    return redirect(
        url_for("dashboard.kick")
    )

@dashboard.route("/ban/run", methods = ["POST"])
@login_required
def run_ban():
    pass