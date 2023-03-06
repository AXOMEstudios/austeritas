from ..helpers import load_json
from ..constants import DATA_FILENAME
from . import login

def test_no_input(client):
    response = client.post("/support/appeal", data = {})
    assert response.status_code == 400

def test_wrong_input(client):
    response = client.post("/support/appeal", data = {
        "player": "_$)%/FEUBIUFB"
    })
    assert response.status_code == 400

def test_not_banned(client):
    response = client.post("/support/appeal", data = {
        "player": "NONEXISTENT"
    })
    assert response.status_code == 400

def test_correct_appeal(client):
    response = client.post("/support/appeal", data = {
        "player": "BannedPlayer",
        "reason": "Example testing reason"
    })
    assert response.status_code == 200

    assert "BannedPlayer" in load_json(DATA_FILENAME)["appeals"].keys()

def test_resend_rejected_appeal(client):
    response = client.post("/support/appeal", data = {
        "player": "Appeal3",
        "reason": "Example testing reason"
    })
    assert response.status_code == 403

def test_accept_appeal(client):
    with client:
        login(client)

        response = client.post("/dashboard/player_support/process/appeal", data = {
            "decision": "approve",
            "player": "Appeal1"
        })
        assert response.status_code == 200

        _tmp = load_json(DATA_FILENAME)
        assert not "Appeal1" in _tmp["appeals"].keys()
        assert not "Appeal1" in _tmp["admin_responses"].keys()
        assert not "Appeal1" in _tmp["bans"].keys()

def test_deny_appeal(client):
    with client:
        login(client)

        response = client.post("/dashboard/player_support/process/appeal", data = {
            "decision": "reject",
            "player": "Appeal2"
        })

        assert response.status_code == 200

        _tmp = load_json(DATA_FILENAME)
        assert not "Appeal2" in _tmp["appeals"].keys()
        assert "Appeal2" in _tmp["bans"].keys()
        assert _tmp["admin_responses"]["Appeal2"] == "rejected"

def test_suspicious_decision(client):
    with client:
        login(client)

        response = client.post("/dashboard/player_support/process/appeal", data = {
            "decision": "invalid",
            "player": "Player"
        })

        assert response.status_code == 302