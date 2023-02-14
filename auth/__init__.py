from flask import Blueprint, render_template, redirect, url_for, session, g, request, flash
import base64, bcrypt, hashlib
from ..helpers import load_json
from ..constants import DUMMY_HASH
from json import dumps

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

@auth.route("/login/submit", methods = ["POST"])
def run_login():
    data = request.form
    users = load_json()["users"]

    for user in users:
        if user["name"] == data["name"]:
            if check_password(data["password"], user["password"]):
                session["user"] = user["name"]
                g.user = user["name"]
                return redirect(url_for("dashboard.home"))
            else:
                flash("Incorrect username or password.", "danger")
                return redirect(url_for("auth.login"))
    else:
        check_password(data["password"], DUMMY_HASH) # just there to mitigate enumeration attacks
        flash("Incorrect username or password.", "danger")
        return redirect(url_for("auth.login"))

@auth.route("/new", methods = ["POST"])
def new_user():
    data = request.form

    json = dumps({
        "name": data["name"],
        "password": generate_password_hash(data["password"])
    })
    flash("Paste this JSON into the user list of your austeritas_config.json file, then restart the server: " + json, "success")
    return redirect(
        url_for("auth.login")
    )

@auth.route("/logout")
def logout():
    del session["user"]
    g.user = ""
    return redirect(
        url_for("main.homepage")
    )