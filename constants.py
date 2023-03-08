# --- constants.py ---
# Edit this file to change the configuration of your Austeritas setup.
# You may need to restart your server in order to make the changes take effect.

# GENERAL AUSTERITAS SETUP
SERVER_NAME                             = "UwU-Server"
SCREEN_PROCESS_NAME                     = "bedrock-server"
LANGUAGE                                = "de"                                                              # supported: en, de
ALLOW_NEW_USERS                         = False                                                             # recommended: False
CLOCK_INTERVAL                          = 10 * 60                                                           # recommended: 600s

# LIMITS
APPEAL_LIMIT                            = "20/hour"
MESSAGE_LIMIT                           = "30/hour"
MAX_CONTENT_SIZE                        = 10 * 1024                                                         # 10 KB

#
# ### ADVANCED SETTINGS ###
# 
# Don't touch those unless you know what you are doing as these can easily break Austeritas' functionality.

# SERVER DEVELOPMENT
DEBUG                                   = False
HAS_HTTPS                               = False

# FILENAMES
CONFIG_FILENAME                         = "austeritas_config.json"
DATA_FILENAME                           = "austeritas_data.json"

# MISCELLANEOUS
DUMMY_HASH                              = "$2b$12$s3YEAcxEsggkbib5uAvfiueIdBho7HfZpgh8OH96qiGUgp5AjB3Lq"    # this is the hash of an empty string ("")
UPDATE_URL                              = "https://raw.githubusercontent.com/AXOMEstudios/austeritas/master/global_bans/"   # used to fetch global ban list updates from GitHub.