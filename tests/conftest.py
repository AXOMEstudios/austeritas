import os
import time

import pytest

from .. import create_app
from ..src.constants import CONFIG_FILENAME, DATA_FILENAME, DUMMY_HASH
from ..src.helpers import load_json, write_json

SWAPPATH = ".dbswap"

DATA_SKELETON = {
    "known_players": [
        "player"
    ],
    "warnings": {},
    "bans": {
        "BannedPlayer": time.time() + 10 * 60,
        "Appeal1": time.time() + 10 * 60,
        "Appeal2": time.time() + 10 * 60,
        "Appeal3": "permanent"
    },
    "appeals": {
        "Appeal1": "Message1",
        "Appeal2": "Message2"
    },
    "messages": [],
    "admin_responses": {
        "Appeal3": "rejected"
    }
}

CONFIG_SKELETON = {
    "users": [
        {
            "name": "tester",
            "password": DUMMY_HASH
        }
    ],
    "autoban_settings": {
        "do_autoban": "off",
        "reset_warns": "on",
        "max_warnings": 3,
        "duration-dimension": "days",
        "duration": 2
    }
}

def setup_test_db():
    def prepare_swap_dir():
        if not os.path.exists(SWAPPATH):
            os.makedirs(SWAPPATH)

    old_data = load_json(DATA_FILENAME)
    old_config = load_json(CONFIG_FILENAME)
    prepare_swap_dir()

    write_json(old_data, os.path.join(SWAPPATH, DATA_FILENAME))
    write_json(old_config, os.path.join(SWAPPATH, CONFIG_FILENAME))

    write_json(DATA_SKELETON,DATA_FILENAME)
    write_json(CONFIG_SKELETON, CONFIG_FILENAME)

def revert_db():
    if not os.path.exists(SWAPPATH):
        write_json({}, CONFIG_FILENAME)
        write_json({}, DATA_FILENAME)
        raise FileNotFoundError("FATAL: Couldn't revert testing environment as the database swap went missing while performing tests.")
    
    write_json(load_json(os.path.join(SWAPPATH, CONFIG_FILENAME)), CONFIG_FILENAME)
    write_json(load_json(os.path.join(SWAPPATH, DATA_FILENAME)), DATA_FILENAME)

@pytest.fixture()
def app():
    setup_test_db()
    yield create_app(testing = True)
    revert_db()

@pytest.fixture()
def client(app):
    return app.test_client()
