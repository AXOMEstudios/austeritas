from requests import get
from ..constants import UPDATE_URL
from json import dump, load
from os import path
from .constants import LIST_NAME, LIST_CHECKSUM_NAME

l = []
def load_list():
    global l
    with open(path.join("global_bans", LIST_NAME), "r") as f:
        l = load(f)
        l = [i.casefold() for i in l]

def check_for_update():
    print("[GLOBAL BANS] Checking for updates.")
    
    checksum = get(UPDATE_URL + LIST_CHECKSUM_NAME).text

    with open(path.join("global_bans", LIST_CHECKSUM_NAME), "r") as f:
        current_checksum = f.read()

    return current_checksum != checksum

def run_update():
    print("[GLOBAL BANS] Found new version of list on GitHub. Installing update.")

    new_list = get(UPDATE_URL + LIST_NAME).json()
    new_checksum = get(UPDATE_URL + LIST_CHECKSUM_NAME).text

    with open(path.join("global_bans", LIST_NAME), "w") as f:
        dump(new_list, f, indent = 4)

    with open(path.join("global_bans", LIST_CHECKSUM_NAME), "w") as f:
        f.write(new_checksum)
    
    print("[GLOBAL BANS] Done. Reading new list.")
    load_list()

def is_banned(player):
    return player.casefold() in l

load_list()