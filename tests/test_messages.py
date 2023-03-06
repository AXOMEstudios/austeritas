from ..helpers import load_json
from ..constants import DATA_FILENAME
from . import login

def _verify_no_entry_in_db(message):
    return (not message in load_json(DATA_FILENAME)["messages"])

def test_no_input(client):
    response = client.post("/support/message", data = {
        "message": ""
    })
    assert response.status_code == 200
    assert _verify_no_entry_in_db("")

def test_too_short_input(client):
    response = client.post("/support/message", data = {
        "message": "abc"
    })
    assert response.status_code == 200
    assert _verify_no_entry_in_db("abc")

def test_too_long_input(client):
    _str = "a" * (3 * 1024 + 1)
    response = client.post("/support/message", data = {
        "message": _str
    })
    assert response.status_code == 200
    assert _verify_no_entry_in_db(_str)

def test_correct_input(client):
    _str = "test" * 10
    response = client.post("/support/message", data = {
        "message": _str
    })
    assert response.status_code == 200
    assert not _verify_no_entry_in_db(_str)

def test_remove_message(client):
    _str = "test" * 10
    response = client.post("/support/message", data = {
        "message": _str
    })

    with client:
        login(client)

        response = client.post("/dashboard/player_support/process/message", data = {
            "message": 0
        })

        assert response.status_code == 200
        assert _verify_no_entry_in_db(_str)