from requests import get
from ..constants import UPDATE_URL
from json import dump, load
from os import path
from constants import LIST_NAME, LIST_CHECKSUM_NAME

with open(path.join("global_bans", LIST_NAME), "r") as f:
    l = load(f)

def check_for_update():
    checksum = get(UPDATE_URL + LIST_CHECKSUM_NAME).text

    with open(path.join("global_bans", LIST_CHECKSUM_NAME), "r") as f:
        current_checksum = f.read()

    return current_checksum != checksum

def run_update():
    new_list = get(UPDATE_URL + LIST_NAME).json
    new_checksum = get(UPDATE_URL + LIST_CHECKSUM_NAME).text

    with open(path.join("global_bans", LIST_NAME), "w") as f:
        dump(new_list, f, indent = 4)

    with open(path.join("global_bans", LIST_CHECKSUM_NAME), "w") as f:
        f.write(new_checksum)

def is_banned(player):
    return player in l