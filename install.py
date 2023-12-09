# This script runs some steps in order to install Austeritas for the first use.

import sys
import uuid
from json import dump

from src.constants import CONFIG_FILENAME, DATA_FILENAME, DUMMY_HASH

if not (len(sys.argv) > 1 and sys.argv[1] == "confirm"):
    print('''[WARNING]
    This will overwrite all Austeritas configuration files and therefore remove:
        - bans
        - mod messages
        - known players
        - registered admin credentials
        - autoban settings
        - and other critical data
        
    Are you sure you want to continue?''')
    if input("(y/n) >> ") != "y":
        raise KeyboardInterrupt(
            "Action cancelled."
        )

print("Writing files...")

DATA_SKELETON = {
    "known_players": [],
    "warnings": {},
    "bans": {},
    "appeals": {},
    "messages": [],
    "admin_responses": {},
    "vanished": [],
}

CONFIG_SKELETON = {
    "users": [],
    "autoban_settings": {
        "do_autoban": "off",
        "reset_warns": "on",
        "max_warnings": 3,
        "duration-dimension": "days",
        "duration": 2
    },
    "blocklist": [],
}

with open(DATA_FILENAME, "w") as f:
    dump(DATA_SKELETON, f, indent=4)

with open(CONFIG_FILENAME, "w") as f:
    dump(CONFIG_SKELETON, f, indent=4)

with open(".env", "w") as f:
    f.write("SECRET_KEY=" + str(uuid.uuid4()) + "-" + str(uuid.uuid4()) + '\nCHAT_FILTER_API_KEY=""')

print("Austeritas files have been written successfully.")
