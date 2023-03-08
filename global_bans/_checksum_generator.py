from hashlib import sha1
from os import path
from constants import LIST_NAME, LIST_CHECKSUM_NAME

with open(path.join("global_bans", LIST_NAME), "r") as f:
    d = f.read()

with open(path.join("global_bans", LIST_CHECKSUM_NAME), "w") as f:
    f.write(
        sha1(d.encode()).hexdigest()
    )