from flask import current_app
from datetime import datetime

def _generate_timestamp():
    return "Austeritas " + datetime.now().strftime("[%m.%d.%Y %H:%M:%S] ")

def log(message, level = 1):
    current_app.logger.log(
        level,
        _generate_timestamp() + message
    )

def warn(message):
    current_app.logger.warn(
        _generate_timestamp() + message
    )

def fatal(message):
    current_app.logger.fatal(
        _generate_timestamp() + message
    )

def info(message):
    current_app.logger.info(
        _generate_timestamp() + message
    )