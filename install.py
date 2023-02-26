# This script runs some steps in order to install Austeritas for the first use.

from constants import DATA_FILENAME, CONFIG_FILENAME, DUMMY_HASH
from json import dump

print("[WARNING] This will overwrite all Austeritas configuration files and therefore remove bans, mod messages, known players, registered admin credentials and much more. Are you sure you want to continue? (y/(n))")
if input("(y/n) >>") != "y": raise KeyboardInterrupt
print("Writing files...")

DATA_SKELETON = {
    "known_players": [],
    "warnings": {},
    "bans": {},
    "appeals": {},
    "messages": []
}

CONFIG_SKELETON = {
    "users": [
        {"name": "default", "password": DUMMY_HASH}
    ],
    "autoban_settings": {
        "do_autoban": "off",
        "reset_warns": "on",
        "max_warnings": 3,
        "duration-dimension": "days",
        "duration": 2
    }
}

with open(DATA_FILENAME, "w") as f:
    dump(DATA_SKELETON, f)

with open(CONFIG_FILENAME, "w") as f:
    dump(CONFIG_SKELETON, f)

print("Austeritas files have been written successfully.")