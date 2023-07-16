from ..constants import SERVER_NAME
from flask_babel import gettext
from datetime import datetime

class c:
    bold = "§l"
    light_green = "§a"
    green = "§2"
    red = "§4"
    warning = "§e"
    reset = "§r"

WARNING_MESSAGE_CHAT = f'''{c.red}[Austeritas]{c.reset}: {c.warning}@%s has been warned. The player currently has {c.reset + c.bold}%s{c.reset + c.warning} warnings.'''

KICK_MESSAGE = f'''{c.red}[Austeritas]{c.reset + c.bold + c.warning} You have been kicked from %s. {c.reset + c.light_green} [You are free to re-connect now]'''

KICK_MESSAGE_CHAT = f'''{c.red}[Austeritas]{c.reset}: {c.warning}@%s has been kicked.'''

BAN_MESSAGE = f'''{c.red}[Austeritas]{c.reset + c.bold + c.warning} You have been banned from %s.{c.reset} Ban expires: {c.red}%s {c.reset} [You can re-join upon the end of your ban]'''

BAN_MESSAGE_CHAT = f'''{c.red}[Austeritas]{c.reset}: {c.warning}@%s has been banned (expires: %s).'''

def construct_warning_message_chat(player, warnings):
    return WARNING_MESSAGE_CHAT % (player, warnings)

def construct_kick_message():
    return KICK_MESSAGE % (SERVER_NAME)

def construct_kick_message_chat(player):
    return KICK_MESSAGE_CHAT % (player)

def construct_ban_message(duration = "permanent"):
    duration = datetime.utcfromtimestamp(duration).strftime('%d.%m.%Y %H:%M:%S UTC') if not duration == "permanent" else duration

    return BAN_MESSAGE % (SERVER_NAME, duration)

def construct_ban_message_chat(player, duration = "permanent"):
    duration = datetime.utcfromtimestamp(duration).strftime('%d.%m.%Y %H:%M:%S UTC') if not duration == "permanent" else duration

    return BAN_MESSAGE_CHAT % (player, duration)