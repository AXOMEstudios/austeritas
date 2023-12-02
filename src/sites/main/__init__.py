from flask import Blueprint, render_template, url_for, g, redirect

main = Blueprint("main", __name__)


@main.route("/")
def homepage():
    if not g.user:
        return render_template("main/main.html")
    else:
        return redirect(url_for("dashboard.home"))
