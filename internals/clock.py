import sched, threading, time
from ..constants import CLOCK_INTERVAL, DATA_FILENAME
from ..helpers import load_json, write_json
from .api import execute_unban

s = sched.scheduler()

def clock_tick():
    try:
        _tmp = load_json(DATA_FILENAME)
        if list(_tmp["bans"].keys()):
            to_delete = []
            for player, timestamp in _tmp["bans"].items():
                if timestamp == "permanent":
                    continue
                if time.time() > timestamp:
                    execute_unban(player)
                    to_delete.append(player)

            for player in to_delete:
                del _tmp["bans"][player]
        write_json(_tmp, DATA_FILENAME)
    except Exception as e:
        print("[AUSTERITAS CLOCK ERROR] %s" % str(e))
    s.enter(CLOCK_INTERVAL, 1, clock_tick)

def start_clock():
    s.enter(CLOCK_INTERVAL, 1, clock_tick)
    s.run()

def init_clock():
    t = threading.Thread(target = start_clock, daemon = True)
    t.start()