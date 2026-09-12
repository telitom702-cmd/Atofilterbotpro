import re
import os
from os import environ, getenv
from Script import script


# ============================
# Utility Functions
# ============================

id_pattern = re.compile(r'^-?\d+$')


def is_enabled(value, default):
    value = str(value).strip().lower()
    if value in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value in ["false", "no", "0", "disable", "n"]:
        return False
    return default


def get_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def get_id(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# ============================
# Bot Information Configuration
# ============================

SESSION = environ.get('SESSION', 'royal_search')
API_ID = get_int(environ.get('API_ID', '24776633'), 0)
API_HASH = environ.get('API_HASH', '57b1f632044b4e718f5dce004a988d69')
BOT_TOKEN = environ.get('BOT_TOKEN', '8748178338:AAFkn8pm-ATKP9D8TOJaVKNwhj6LdzzBaKg')


# ============================
# Bot Settings Configuration
# ============================

CACHE_TIME = get_int(environ.get('CACHE_TIME', 300), 300)
USE_CAPTION_FILTER = is_enabled(environ.get('USE_CAPTION_FILTER', 'True'), True)
INDEX_CAPTION = is_enabled(environ.get('SAVE_CAPTION', 'True'), True)

# Making it false will not save caption in DB
# So you can save some storage space

PICS = environ.get('PICS', 'https://graph.org/file/56b5deb73f3b132e2bb73.jpg https://graph.org/file/5303692652d91d52180c2.jpg https://graph.org/file/425b6f46efc7c6d64105f.jpg https://graph.org/file/876867e761c6c7a29855b.jpg').split()

NOR_IMG = environ.get("NOR_IMG", "https://graph.org/file/e20b5fdaf217252964202.jpg")
MELCOW_PHOTO = environ.get("MELCOW_PHOTO", "https://graph.org/file/56b5deb73f3b132e2bb73.jpg")
SPELL_IMG = environ.get("SPELL_IMG", "https://graph.org/file/13702ae26fb05df52667c.jpg")
SUBSCRIPTION = environ.get('SUBSCRIPTION', 'https://graph.org/file/242b7f1b52743938d81f1.jpg')
FSUB_PICS = environ.get('FSUB_PICS', 'https://graph.org/file/7478ff3eac37f4329c3d8.jpg https://graph.org/file/56b5deb73f3b132e2bb73.jpg').split()


# ============================
# Admin, Channels & Users Configuration
# ============================

ADMINS = [get_id(admin) for admin in environ.get('ADMINS', '8248792819').split() if admin.strip()]
CHANNELS = [get_id(ch) for ch in environ.get('CHANNELS', '-1003592579879 -1003036018855 -1004167255440 -1002715303050').split() if ch.strip()]

LOG_CHANNEL = get_id(environ.get('LOG_CHANNEL', '-100308449068'), 0)
BIN_CHANNEL = get_id(environ.get('BIN_CHANNEL', '-100308449068'), 0)
PREMIUM_LOGS = get_id(environ.get('PREMIUM_LOGS', ''), 0)

DELETE_CHANNELS = [get_id(dch) for dch in environ.get('DELETE_CHANNELS', '').split() if dch.strip()]

support_chat_id = environ.get('SUPPORT_CHAT_ID', 'https://t.me/request_gruop')
reqst_channel = environ.get('REQST_CHANNEL_ID', 'https://t.me/jacpotfilmm')
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'https://t.me/request_gruop')

# FORCE_SUB
auth_req_channels = environ.get("AUTH_REQ_CHANNELS", "")
auth_channels = environ.get("AUTH_CHANNELS", "")


# ============================
# Payment Configuration
# ============================

QR_CODE = environ.get('QR_CODE', 'Your_Qr_Code')
OWNER_UPI_ID = environ.get('OWNER_UPI_ID', 'ɴᴏ ᴀᴠᴀɪʟᴀʙʟᴇ ʀɪɢʜᴛ ɴᴏᴡ')

STAR_PREMIUM_PLANS = {
    10: "7day",
    20: "15day",
    40: "1month",
    55: "45day",
    75: "60day",
}


# ============================
# MongoDB Configuration
# ============================

DATABASE_URI = environ.get('DATABASE_URI', 'mongodb+srv://mongodbpy_db_user:pPgtRKyHsm8GvJF2@cluster0.u2ft5ps.mongodb.net/?appName=Cluster0')
DATABASE_NAME = environ.get('DATABASE_NAME', 'Cluster0')
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'royal_files')

# If MULTIPLE_DB is True, fill DATABASE_URI2
MULTIPLE_DB = is_enabled(environ.get('MULTIPLE_DB', 'False'), False)
DATABASE_URI2 = environ.get('DATABASE_URI2', '')


# ============================
# Movie Notification & Update Settings
# ============================

MOVIE_UPDATE_NOTIFICATION = is_enabled(environ.get('MOVIE_UPDATE_NOTIFICATION', 'False'), False)
MOVIE_UPDATE_CHANNEL = get_id(environ.get('MOVIE_UPDATE_CHANNEL', ''), 0)

DREAMXBOTZ_IMAGE_FETCH = is_enabled(environ.get('DREAMXBOTZ_IMAGE_FETCH', 'True'), True)
LINK_PREVIEW = is_enabled(environ.get('LINK_PREVIEW', 'False'), False)
ABOVE_PREVIEW = is_enabled(environ.get('ABOVE_PREVIEW', 'True'), True)

TMDB_API_KEY = environ.get('TMDB_API_KEY', '')
TMDB_POSTER = is_enabled(environ.get('TMDB_POSTER', 'False'), False)
LANDSCAPE_POSTER = is_enabled(environ.get('LANDSCAPE_POSTER', 'True'), True)


# ============================
# Verification Settings
# ============================

IS_VERIFY = is_enabled(environ.get('IS_VERIFY', 'False'), False)

LOG_VR_CHANNEL = get_id(environ.get('LOG_VR_CHANNEL', ''), 0)
LOG_API_CHANNEL = get_id(environ.get('LOG_API_CHANNEL', ''), 0)

VERIFY_IMG = environ.get("VERIFY_IMG", "https://telegra.ph/file/9ecc5d6e4df5b83424896.jpg")

TUTORIAL = environ.get("TUTORIAL", "https://t.me/technokrrish")
TUTORIAL_2 = environ.get("TUTORIAL_2", "https://t.me/technokrrish")
TUTORIAL_3 = environ.get("TUTORIAL_3", "https://t.me/technokrrish")

SHORTENER_API = environ.get("SHORTENER_API", "")
SHORTENER_WEBSITE = environ.get("SHORTENER_WEBSITE", "https://api.gplinks.com")

SHORTENER_API2 = environ.get("SHORTENER_API2", "")
SHORTENER_WEBSITE2 = environ.get("SHORTENER_WEBSITE2", "")

SHORTENER_API3 = environ.get("SHORTENER_API3", "")
SHORTENER_WEBSITE3 = environ.get("SHORTENER_WEBSITE3", "")

TWO_VERIFY_GAP = get_int(environ.get('TWO_VERIFY_GAP', 1200), 1200)
THREE_VERIFY_GAP = get_int(environ.get('THREE_VERIFY_GAP', 54000), 54000)


# ============================
# Channel & Group Links Configuration
# ============================

GRP_LNK = environ.get('GRP_LNK', 'https://t.me/request_gruop')
OWNER_LNK = environ.get('OWNER_LNK', 'https://t.me/request_gruop')
UPDATE_CHNL_LNK = environ.get('UPDATE_CHNL_LNK', 'https://t.me/jacpotfilmm')


# ============================
# User Configuration
# ============================

auth_users = [get_id(user) for user in environ.get('AUTH_USERS', '').split() if user.strip()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else ADMINS

PREMIUM_USER = [get_id(user) for user in environ.get('PREMIUM_USER', '').split() if user.strip()]


# ============================
# Miscellaneous Configuration
# ============================

ULTRA_FAST_MODE = is_enabled(environ.get('ULTRA_FAST_MODE', 'False'), True)

MAX_B_TN = get_int(environ.get("MAX_B_TN", "5"), 5)
PORT = get_int(environ.get("PORT", "8080"), 8080)

MSG_ALRT = environ.get('MSG_ALRT', 'Share & Support Us ♥️')
DELETE_TIME = get_int(environ.get("DELETE_TIME", "300"), 300)

CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", script.CAPTION)
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", script.IMDB_TEMPLATE_TXT)

MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = get_id(environ.get('INDEX_REQ_CHANNEL', str(LOG_CHANNEL)), LOG_CHANNEL)

NO_RESULTS_MSG = is_enabled(environ.get("NO_RESULTS_MSG", "True"), True)
MAX_BTN = is_enabled(environ.get('MAX_BTN', "True"), True)
P_TTI_SHOW_OFF = is_enabled(environ.get('P_TTI_SHOW_OFF', "False"), False)

IMDB = is_enabled(environ.get('IMDB', "False"), False)
TMDB_ON_SEARCH = is_enabled(environ.get('TMDB_ON_SEARCH', "False"), False)

AUTO_FFILTER = is_enabled(environ.get('AUTO_FFILTER', "True"), True)
AUTO_DELETE = is_enabled(environ.get('AUTO_DELETE', "True"), True)

LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MELCOW_NEW_USERS = is_enabled(environ.get('MELCOW_NEW_USERS', "False"), False)
PROTECT_CONTENT = is_enabled(environ.get('PROTECT_CONTENT', "False"), False)

PM_SEARCH = is_enabled(environ.get('PM_SEARCH', "True"), True)
EMOJI_MODE = is_enabled(environ.get('EMOJI_MODE', "False"), False)
BUTTON_MODE = is_enabled(environ.get('BUTTON_MODE', "False"), False)

STREAM_MODE = is_enabled(environ.get('STREAM_MODE', "False"), False)
PREMIUM_STREAM_MODE = is_enabled(environ.get('PREMIUM_STREAM_MODE', "False"), False)


# ============================
# Bot Configuration
# ============================

AUTH_REQ_CHANNELS = [get_id(ch) for ch in auth_req_channels.split() if ch.strip()]
AUTH_CHANNELS = [get_id(ch) for ch in auth_channels.split() if ch.strip()]

REQST_CHANNEL = get_id(reqst_channel, 0) if reqst_channel else None
SUPPORT_CHAT_ID = get_id(support_chat_id, 0) if support_chat_id else None

LANGUAGES = {"ᴍᴀʟᴀʏᴀʟᴀᴍ": "mal", "ᴛᴀᴍɪʟ": "tam", "ᴇɴɢʟɪsʜ": "eng", "ʜɪɴᴅɪ": "hin", "ʙᴀɴɢʟᴀ": "bengali", "ᴛᴇʟᴜɢᴜ": "tel", "ᴋᴀɴɴᴀᴅᴀ": "kan", "ɢᴜᴊᴀʀᴀᴛɪ": "guj", "ᴍᴀʀᴀᴛʜɪ": "mar", "ᴘᴜɴᴊᴀʙɪ": "pun"}

QUALITIES = ["360P", "480P", "720P", "1080P", "1440P", "2160P", "4K"]

SEASON_COUNT = 12
SEASONS = [f"S{str(i).zfill(2)}" for i in range(1, SEASON_COUNT + 1)]

BAD_WORDS = {
    "PrivateMovieZ",
    "toonworld4all",
    "themoviesboss",
    "1tamilmv",
    "tamilblasters",
    "1tamilblasters",
    "skymovieshd",
    "extraflix",
    "hdm2",
    "moviesmod",
    "hdhub4u",
    "mkvcinemas",
    "primefix",
    "join",
    "www",
    "villa",
    "tg",
    "original"
}


# ============================
# Server & Web Configuration
# ============================

NO_PORT = is_enabled(environ.get('NO_PORT', 'False'), False)

APP_NAME = environ.get('APP_NAME', None)
ON_HEROKU = 'DYNO' in environ

if ON_HEROKU:
    APP_NAME = environ.get('APP_NAME', APP_NAME)

BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))

if ON_HEROKU:
    FQDN = str(getenv('FQDN', f'{APP_NAME}.herokuapp.com' if APP_NAME else 'localhost'))
else:
    FQDN = str(getenv('FQDN', BIND_ADRESS))

SLEEP_THRESHOLD = get_int(environ.get('SLEEP_THRESHOLD', '60'), 60)
WORKERS = get_int(environ.get('WORKERS', '4'), 4)
SESSION_NAME = str(environ.get('SESSION_NAME', 'dreamXBotz'))
MULTI_CLIENT = False
name = str(environ.get('name', 'DREAMXBOTZ'))
PING_INTERVAL = get_int(environ.get("PING_INTERVAL", "1200"), 1200)

HAS_SSL = is_enabled(environ.get('HAS_SSL', 'True'), True)

if HAS_SSL:
    URL = f"https://{FQDN}/"
else:
    URL = f"http://{FQDN}/"


# ============================
# Reactions Configuration
# ============================

REACTIONS = ["🤝", "😇", "🤗", "😍", "👍", "🎅", "😐", "🥰", "🤩", "😱", "🤣", "😘", "👏", "😛", "😈", "🎉", "⚡️", "🫡", "🤓", "😎", "🏆", "🔥", "🤭", "🌚", "🆒", "👻", "😁"]


# ============================
# Commands Bot
# ============================

Bot_cmds = {
    "start": "Sᴛᴀʀᴛ Mᴇ Bᴀʙʏ",
    "stats": "Gᴇᴛ Bᴏᴛ Sᴛᴀᴛs",
    "alive": " Cʜᴇᴄᴋ Bᴏᴛ Aʟɪᴠᴇ ᴏʀ Nᴏᴛ ",
    "settings": "ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs",
    "id": "ɢᴇᴛ ɪᴅ ᴛᴇʟᴇɢʀᴀᴍ ",
    "info": "Gᴇᴛ Usᴇʀ ɪɴғᴏ ",
    "del_msg": "ʀᴇᴍᴏᴠᴇ ғɪʟᴇ ɴᴀᴍᴇ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ɴᴏтɪғɪᴄᴀᴛɪᴏɴ...",
    "movie_update": "ᴏɴ ᴏғғ ᴀᴄᴄᴏʀᴅɪɴɢ ʏᴏᴜʀ ɴᴇᴇᴅᴇᴅ...",
    "pm_search": "ᴘᴍ sᴇᴀʀᴄʜ ᴏɴ ᴏғғ ᴀᴄᴄᴏʀᴅɪɴɢ ʏᴏᴜʀ ɴᴇᴇᴅᴇᴅ...",
    "trendlist": "Gᴇᴛ Tᴏᴘ Tʀᴇɴᴅɪɴɢ Sᴇᴀʀᴄʜ Lɪsᴛ",
    "broadcast": "ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀꜱ.",
    "grp_broadcast": "ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘs",
    "send": "ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀ ᴘᴀʀᴛɪᴄᴜʟᴀʀ ᴜꜱᴇʀ.",
    "add_premium": "ᴀᴅᴅ ᴀɴʏ ᴜꜱᴇʀ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ.",
    "remove_premium": "ʀᴇᴍᴏᴠᴇ ᴀɴʏ ᴜꜱᴇʀ ꜰʀᴏᴍ ᴘʀᴇᴍɪᴜᴍ.",
    "premium_users": "ɢᴇᴛ ʟɪsᴛ ᴏꜰ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ.",
    "restart": "ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ.",
    "group_cmd": "ɢʀᴏᴜᴘ ᴄᴏᴍᴍᴀɴᴅ ʟɪsᴛ",
    "admin_cmd": "ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs ʟɪsᴛ.",
    "reset_group": "Group Setting Default",
    "trial_reset": "User Trial Reset"
}


# ============================
# Multiple Database Configuration
# ============================

if MULTIPLE_DB is False:
    DATABASE_URI2 = DATABASE_URI
else:
    DATABASE_URI2 = environ.get('DATABASE_URI2', '')


# ============================
# Logs Configuration
# ============================

LOG_STR = "Current Customized Configurations are:-\n"

LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for your queries.\n" if IMDB else "IMDB Results are disabled.\n")

LOG_STR += ("P_TTI_SHOW_OFF found, Users will be redirected to send /start to Bot PM instead of sending file directly.\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled, files will be sent in PM instead of starting the bot.\n")

LOG_STR += ("BUTTON_MODE is found, filename and file size will be shown in a single button instead of two separate buttons.\n" if BUTTON_MODE else "BUTTON_MODE is disabled, filename and file size will be shown as different buttons.\n")

LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be sent along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")

LOG_STR += ("Long IMDB storyline enabled.\n" if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled, Plot will be shorter.\n")

LOG_STR += ("Spell Check Mode is enabled, bot will be suggesting related movies if movie name is misspelled.\n" if SPELL_CHECK_REPLY else "Spell Check Mode is disabled.\n")
