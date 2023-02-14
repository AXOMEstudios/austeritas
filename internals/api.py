from ..helpers import load_json, write_json
from ..constants import DATA_FILENAME
from .messageconstructor import construct_ban_message, construct_ban_message_chat, construct_kick_message, construct_kick_message_chat, construct_warning_message_chat
from subprocess import Popen

SKIP_COMMANDS = False # TODO: CHANGE before production to FALSE - otherwise, none of the actions will take effect.

def type_into_server_console(command):
    if SKIP_COMMANDS: return
    Popen([
        "/usr/bin/screen",
        "-Rd",
        "bedrock-server",
        "-X",
        "stuff",
        "%s \r" % command
    ])

def execute_kick(player):
    commands_to_execute = [
        "kick %s %s" % (player, construct_kick_message()),
        "say %s" % construct_kick_message_chat(player)
    ]

    for command in commands_to_execute:
        type_into_server_console(command)

def execute_ban(player, duration = "permanent"):
    commands_to_execute = [
        "kick %s %s" % (player, construct_ban_message(duration)),
        "allowlist remove %s" % player,
        "say %s" % construct_ban_message_chat(player, duration)
    ]

    for command in commands_to_execute:
        type_into_server_console(command)

    if duration != "permanent":
        _tmp = load_json(DATA_FILENAME)
        _tmp["bans"][player] = duration
        write_json(_tmp, DATA_FILENAME)

def execute_unban(player):
    type_into_server_console(
        "allowlist add %s" % player
    )

def send_chat_warning(player, warnings):
    type_into_server_console(
        "say %s" % construct_warning_message_chat(player, warnings)
    )