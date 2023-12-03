import sys
from subprocess import Popen

from ..constants import DATA_FILENAME, DEBUG, SCREEN_PROCESS_NAME
from ..global_bans import check_for_update, run_update
from ..helpers import load_json, validate_player_name, write_json
from .messageconstructor import (construct_ban_message,
                                 construct_ban_message_chat,
                                 construct_kick_message,
                                 construct_kick_message_chat,
                                 construct_warning_message_chat)

SKIP_COMMANDS = False
if "pytest" in sys.modules or DEBUG:
    SKIP_COMMANDS = True


def type_into_server_console(command):
    if SKIP_COMMANDS:
        return
    Popen([
        "/usr/bin/screen",
        "-Rd",
        SCREEN_PROCESS_NAME,
        "-X",
        "stuff",
        "%s \r" % command
    ])


def execute_kick(player):
    if not validate_player_name(player):
        return

    commands_to_execute = [
        "kick %s %s" % (player, construct_kick_message()),
        "say %s" % construct_kick_message_chat(player)
    ]

    for command in commands_to_execute:
        type_into_server_console(command)


def execute_ban(player, duration="permanent"):
    if not validate_player_name(player):
        return

    commands_to_execute = [
        "kick %s %s" % (player, construct_ban_message(duration)),
        "allowlist remove %s" % player,
        "say %s" % construct_ban_message_chat(player, duration)
    ]

    for command in commands_to_execute:
        print(command)
        type_into_server_console(command)

    _tmp = load_json(DATA_FILENAME)
    _tmp["bans"][player] = duration
    write_json(_tmp, DATA_FILENAME)


def execute_unban(player):
    if not validate_player_name(player):
        return

    type_into_server_console(
        "allowlist add %s" % player
    )


def send_chat_warning(player, warnings):
    if not validate_player_name(player):
        return

    type_into_server_console(
        "say %s" % construct_warning_message_chat(player, warnings)
    )


def send_private_message(player, text):
    if not validate_player_name(player):
        return

    print("tellraw %s %s" % (player, text))
    type_into_server_console(
        "tellraw %s %s" % (player, text)
    )


def whitelist_operation(player, mode="add"):
    if not mode in ["add", "remove"]:
        return
    if not validate_player_name(player):
        return

    type_into_server_console(
        "allowlist %s %s" % (mode, player)
    )


def banlist_update_tick():
    if check_for_update():
        run_update()
