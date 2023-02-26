from flask import Blueprint, render_template, request, url_for, flash, redirect
from ..helpers import login_required, load_json, write_json, validate_player_name
from ..constants import DATA_FILENAME, CONFIG_FILENAME, CLOCK_INTERVAL
from ..internals.api import execute_kick, execute_ban, send_chat_warning, execute_unban, whitelist_operation
import time
from datetime import datetime
from flask_babel import gettext

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")

DIMENSIONS_TRANSLATED = {
    "minutes": 60,
    "hours": 60 * 60,
    "days": 60 * 60 * 24,
    "weeks": 60 * 60 * 24 * 7,
    "months": 60 * 60 * 24 * 31,
    "permanent": -1
}

def add_to_list_of_known_players(player):
    _tmp = load_json(DATA_FILENAME)
    if not player in _tmp["known_players"]:
        _tmp["known_players"].append(player)
        write_json(_tmp, DATA_FILENAME)
        flash(gettext("Added player to list of known players."), "success")
    else:
        flash(gettext("Player already on list."), "danger")

def remove_from_list_of_known_players(player):
    _tmp = load_json(DATA_FILENAME)
    if player in _tmp["known_players"]:
        _tmp["known_players"].remove(player)
        write_json(_tmp, DATA_FILENAME)
        flash(gettext("Removed player from list of known players."), "success")
    else:
        flash(gettext("Player not found on list."), "danger")

def add_warning_to_player(player):
    _tmp = load_json(DATA_FILENAME)
    autoban_settings = load_json(CONFIG_FILENAME)["autoban_settings"]

    if not player in _tmp["warnings"]:
        _tmp["warnings"][player] = 1
    else:
        _tmp["warnings"][player] += 1
    send_chat_warning(player, _tmp["warnings"][player])
    flash(gettext("Gave one warning to %s") % player, "success")
    write_json(_tmp, DATA_FILENAME)

    if autoban_settings["do_autoban"] == "on":
        if _tmp["warnings"][player] >= autoban_settings["max_warnings"]:
            duration_in_seconds = int(autoban_settings["duration"]) * DIMENSIONS_TRANSLATED[
                autoban_settings["duration-dimension"]
            ]
            ban_end_timestamp = round(time.time()) + duration_in_seconds
    
            execute_ban(player, (ban_end_timestamp if duration_in_seconds > 0 else "permanent"))
            flash(gettext("Automatic banning: %s banned (%s%s) for exceeding warning limit of %s warnings.") % (
                player,
                (autoban_settings["duration"] if not autoban_settings["duration-dimension"] == "permanent" else ""),
                (" " if not autoban_settings["duration-dimension"] == "permanent" else "") + autoban_settings["duration-dimension"],
                autoban_settings["max_warnings"]
            ), "warning")

            if autoban_settings["reset_warns"] == "on":
                _tmp = load_json(DATA_FILENAME)
                del _tmp["warnings"][player]
                write_json(_tmp, DATA_FILENAME)
                flash(gettext("Automatic banning: Removed all warnings from %s due to policy.") % player, "warning")


def remove_warning_from_player(player):
    _tmp = load_json(DATA_FILENAME)
    if not player in _tmp["warnings"]:
        flash(gettext("The player has no warnings."), "danger")
        return
    else:
        if _tmp["warnings"][player] > 1:
            _tmp["warnings"][player] -= 1
        else:
            del _tmp["warnings"][player]

    write_json(_tmp, DATA_FILENAME)
    flash(gettext("Removed one warning from %s.") % player, "success")

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
    banned_players = load_json(DATA_FILENAME)["bans"]
    banned_players = {
        player: (datetime.utcfromtimestamp(expiration).strftime('%d.%m.%Y %H:%M:%S UTC') if expiration != "permanent" else "permanent") for player, expiration in banned_players.items()
    }
    return render_template("dashboard/ban.html", list_of_players = known, banned_players = banned_players, clock_rate = round(CLOCK_INTERVAL / 60))

@dashboard.route("/warnings")
@login_required
def warnings():
    _tmp = load_json(DATA_FILENAME)
    warnings = _tmp["warnings"]
    known = _tmp["known_players"]
    return render_template("dashboard/warnings.html", warnings = warnings, list_of_players = known)

@dashboard.route("/etc")
@login_required
def etc():
    known = load_json(DATA_FILENAME)["known_players"]
    autoban_settings = load_json(CONFIG_FILENAME)["autoban_settings"]
    return render_template("dashboard/etc.html", list_of_players = known, clock_rate = round(CLOCK_INTERVAL / 60), abs = autoban_settings)

@dashboard.route("/kick/run", methods = ["POST"])
@login_required
def run_kick():
    data = request.form
    if not data["player"]:
        flash(gettext("You must provide a player name."), "danger")
        return redirect(
            url_for("dashboard.kick")
        )

    if not validate_player_name(data["player"]):
        flash(gettext("Invalid input.", "danger"))
        return redirect(
            url_for("dashboard.kick")
        )

    if "remember" in data.keys() and data["remember"] == "on":
        add_to_list_of_known_players(data["player"])

    if "warn" in data.keys() and data["warn"] == "on":
        add_warning_to_player(data["player"])

    execute_kick(data["player"])
    flash(gettext("Sent kick signal to server."), "success")

    return redirect(
        url_for("dashboard.kick")
    )

@dashboard.route("/ban/run", methods = ["POST"])
@login_required
def run_ban():
    data = request.form
    if not data["player"]:
        flash(gettext("You must provide a player name."), "danger")
        return redirect(
            url_for("dashboard.ban")
        )

    if "remember" in data.keys() and data["remember"] == "on":
        add_to_list_of_known_players(data["player"])

    if not data["duration-dimension"] in DIMENSIONS_TRANSLATED.keys():
        flash(gettext("Choose a correct dimension."), "danger")
        return redirect(url_for("dashboard.ban"))
    
    if data["duration-dimension"] != "permanent" and (not data["duration"]):
        flash(gettext("Enter a time."), "danger")
        return redirect(url_for("dashboard.ban"))
    
    res_duration = 0
    if data["duration-dimension"] == "permanent":
        res_duration = 1
    else:
        res_duration = data["duration"]

    duration_in_seconds = int(res_duration) * DIMENSIONS_TRANSLATED[
        data["duration-dimension"]
    ]
    ban_end_timestamp = round(time.time()) + duration_in_seconds
    
    execute_ban(data["player"], (ban_end_timestamp if duration_in_seconds > 0 else "permanent"))
    flash(gettext("Player banned for %s %s.") % (data["duration"], data["duration-dimension"])
          if data["duration-dimension"] != "permanent" else gettext("Player banned permanently."), "success")
    
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

@dashboard.route("/etc/autoban", methods = ["POST"])
@login_required
def auto_ban():
    data = request.form

    if not (data["max_warnings"] and data["duration"]):
        flash(gettext("Fill out all the fields!"), "danger")
        return redirect(
            url_for("dashboard.etc")
        )

    settings = {
        "do_autoban": "on" if "do_autoban" in data.keys() else "off",
        "reset_warns": "on" if "reset_warns" in data.keys() else "off",
        "max_warnings": int(data["max_warnings"]),
        "duration-dimension": data["duration-dimension"],
        "duration": (int(data["duration"]) if data["duration-dimension"] != "permanent" else 1)
    }

    if not data["duration-dimension"] in DIMENSIONS_TRANSLATED.keys():
        flash(gettext("Please enter a valid duration dimension."), "danger")
        return redirect(
            url_for("dashboard.etc")
        )

    _tmp = load_json(CONFIG_FILENAME)
    _tmp["autoban_settings"] = settings
    write_json(_tmp, CONFIG_FILENAME)

    flash(gettext("Automatic banning: Settings saved."), "success")

    return redirect(
        url_for("dashboard.etc")
    )

@dashboard.route("/ban/unban", methods = ["POST"])
@login_required
def run_unban():
    data = request.form
    execute_unban(data["player"])

    _tmp = load_json(DATA_FILENAME)
    expiration = _tmp["bans"][data["player"]]
    del _tmp["bans"][data["player"]]
    write_json(_tmp, DATA_FILENAME)
    
    if expiration != "permanent":
        flash(gettext("%s has been unbanned. Otherwise, the ban would've ended on %s.") % (data["player"], datetime.utcfromtimestamp(expiration).strftime('%d.%m.%Y %H:%M:%S UTC')), "success")
    else:
        flash(gettext("%s has been unbanned. Otherwise, the ban would've never ended.") % data["player"], "success")

    return redirect(
        url_for("dashboard.ban")
    )

@dashboard.route("/etc/edit_whitelist", methods = ["POST"])
@login_required
def edit_whitelist():
    data = request.form

    if not "mode" in data.keys():
        flash(gettext("Provide an operation mode."), "danger")
    elif (not "player" in data.keys()) or (not data["player"]) or (not validate_player_name(data["player"])):
        flash(gettext("Provide a valid player name."), "danger")
    else:
        whitelist_operation(
            data["player"],
            data["mode"]
        )
        flash(gettext("Successfully sent editing request to server."), "success")

    return redirect(
        url_for("dashboard.etc")
    )

@dashboard.route("/player_support/")
@login_required
def player_support():
    pass