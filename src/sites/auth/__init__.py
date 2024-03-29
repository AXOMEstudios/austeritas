from flask import Blueprint, render_template, redirect, url_for, session, g, request, flash
import base64
import bcrypt
import hashlib
from ...helpers import load_json, login_required
from ...constants import DUMMY_HASH, ALLOW_NEW_USERS
from json import dumps
from flask_babel import gettext

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.before_app_request
def before_main_request():
    if "user" in session.keys():
        g.user = session["user"]
    else:
        g.user = ""


def generate_password_hash(password):
    password = password.encode("utf-8")
    password = base64.b64encode(hashlib.sha256(password).digest())
    hashed = bcrypt.hashpw(
        password,
        bcrypt.gensalt()
    ).decode()
    return hashed


def check_password(password, hash):
    password = password.encode("utf-8")
    password = base64.b64encode(hashlib.sha256(password).digest())
    hash = hash.encode("utf-8")
    return bcrypt.checkpw(password, hash)


@auth.route("/login")
def login():
    return render_template("/auth/login.html")


@auth.route("/login/submit", methods=["POST"])
def run_login():
    data = request.form
    users = load_json()["users"]

    for user in users:
        if user["name"] == data["name"]:
            if check_password(data["password"], user["password"]):
                session["user"] = user["name"]
                g.user = user["name"]
                return redirect(url_for("dashboard.home")), 200
            else:
                flash(gettext("Incorrect username or password."), "danger")
                return redirect(url_for("auth.login")), 403
    else:
        # just there to mitigate enumeration attacks
        check_password(data["password"], DUMMY_HASH)
        flash(gettext("Incorrect username or password."), "danger")
        return redirect(url_for("auth.login")), 403


@auth.route("/new", methods=["POST"])
def new_user():
    data = request.form

    if not ALLOW_NEW_USERS:
        flash("Signup disabled.", "danger")
        return redirect(
            url_for("auth.login")
        ), 403

    json = dumps({
        "name": data["name"],
        "password": generate_password_hash(data["password"])
    })
    flash(gettext("Paste this JSON into the user list of your austeritas_config.json file, then restart the server: ") + json, "success")
    return redirect(
        url_for("auth.login")
    )


@auth.route("/logout")
@login_required
def logout():
    del session["user"]
    g.user = ""
    return redirect(
        url_for("main.homepage")
    )
