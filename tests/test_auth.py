from ..constants import ALLOW_NEW_USERS
from ..route_definitions import PUBLIC_ROUTES, UNPROTECTED_ROUTES
from flask import url_for, session
from . import login

def test_new_user(client):
    response = client.post("/auth/new", data = {
        "name": "tester",
        "password": ""
    })

    if ALLOW_NEW_USERS:
        assert response.status_code == 200
    else:
        assert response.status_code == 403


def test_login_required(client, app):
    with app.test_request_context():
        routes = [
            (url_for(rule.endpoint) if "GET" in rule.methods and rule.endpoint != "static" else "") for rule in app.url_map.iter_rules()
        ]

    for route in routes:
        if route in PUBLIC_ROUTES + UNPROTECTED_ROUTES: continue
        if route == "": continue

        response = client.get(route)
        assert response.status_code == 401

def test_no_user(client):
    response = client.post("/auth/login/submit", data = {
        "name": "inexistent",
        "password": ""
    })

    assert response.status_code == 403

def test_wrong_password(client):
    response = client.post("/auth/login/submit", data = {
        "name": "tester",
        "password": "1234"
    })

    assert response.status_code == 403

def test_login(client):
    with client:
        response = login(client)

        assert response.status_code == 200
        assert session["user"] == "tester"

def test_login_logout(client):
    with client:
        login(client)

        response = client.get("/auth/logout")
        assert response.status_code == 302

        response = client.get("/dashboard/")
        assert response.status_code == 401