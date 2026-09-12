import os
import re
from os import environ, getenv

from Script import script


# =========================================================
# Utility Functions
# =========================================================

id_pattern = re.compile(r"^-?\d+$")


def is_enabled(value, default=False):
    """
    Environment variable থেকে সঠিক Boolean value তৈরি করে।
    """
    if value is None:
        return default

    value = str(value).strip().lower()

    if value in ("true", "yes", "1", "enable", "enabled", "y", "on"):
        return True

    if value in ("false", "no", "0", "disable", "disabled", "n", "off"):
        return False

    return default


def get_int_list(value, default=None):
    """
    Space অথবা comma দিয়ে দেওয়া ID list কে integer list করে।
    """
    if not value:
        return default or []

    result = []

    for item in re.split(r"[\s,]+", str(value).strip()):
        if not item:
            continue

        try:
            result.append(int(item))
        except ValueError:
            result.append(item)

    return result


def get_channel_list(value):
    """
    Valid Telegram numeric channel/group ID only রাখে।
    """
    if not value:
        return []

    result = []

    for item in re.split(r"[\s,]+", str(value).strip()):
        if not item:
            continue

        if id_pattern.fullmatch(item):
            result.append(int(item))

    return result


# =========================================================
# Bot Information Configuration
# =========================================================

SESSION = environ.get("SESSION", "royal_search")

API_ID = int(environ.get("API_ID", "24776633"))

API_HASH = environ.get(
    "API_HASH",
    "57b1f632044b4e718f5dce004a988d69"
)

BOT_TOKEN = environ.get(
    "BOT_TOKEN",
    "8748178338:AAFkn8pm-ATKP9D8TOJaVKNwhj6LdzzBaKg"
)


# =========================================================
# Bot Settings Configuration
# =========================================================

CACHE_TIME = int(environ.get("CACHE_TIME", "300"))

USE_CAPTION_FILTER = is_enabled(
    environ.get("USE_CAPTION_FILTER"),
    True
)

INDEX_CAPTION = is_enabled(
    environ.get("SAVE_CAPTION"),
    True
)


# =========================================================
# Images Configuration
# =========================================================

PICS = environ.get(
    "PICS",
    (
        "https://graph.org/file/56b5deb73f3b132e2bb73.jpg "
        "https://graph.org/file/5303692652d91d52180c2.jpg "
        "https://graph.org/file/425b6f46efc7c6d64105f.jpg "
        "https://graph.org/file/876867e761c6c7a29855b.jpg"
    )
).split()

NOR_IMG = environ.get(
    "NOR_IMG",
    "https://graph.org/file/e20b5fdaf217252964202.jpg"
)

MELCOW_PHOTO = environ.get(
    "MELCOW_PHOTO",
    "https://graph.org/file/56b5deb73f3b132e2bb73.jpg"
)

SPELL_IMG = environ.get(
    "SPELL_IMG",
    "https://graph.org/file/13702ae26fb05df52667c.jpg"
)

SUBSCRIPTION = environ.get(
    "SUBSCRIPTION",
    "https://graph.org/file/242b7f1b52743938d81f1.jpg"
)

FSUB_PICS = environ.get(
    "FSUB_PICS",
    (
        "https://graph.org/file/7478ff3eac37f4329c3d8.jpg "
        "https://graph.org/file/56b5deb73f3b132e2bb73.jpg"
    )
).split()


# =========================================================
# Admin, Channels & Users Configuration
# =========================================================

ADMINS = get_int_list(
    environ.get("ADMINS", "8248792819")
)

CHANNELS = get_int_list(
    environ.get(
        "CHANNELS",
        "-1003036018855 -1003086003339 "
        "-1002715303050 -1004167255440"
    )
)

LOG_CHANNEL = int(
    environ.get("LOG_CHANNEL", "-1003084490680")
)

BIN_CHANNEL = int(
    environ.get("BIN_CHANNEL", "-1003084490680")
)

PREMIUM_LOGS = int(
    environ.get("PREMIUM_LOGS", "-100")
)

DELETE_CHANNELS = get_int_list(
    environ.get("DELETE_CHANNELS", "")
)

support_chat_id = environ.get(
    "SUPPORT_CHAT_ID",
    ""
)

reqst_channel = environ.get(
    "REQST_CHANNEL_ID",
    ""
)

SUPPORT_CHAT = environ.get(
    "SUPPORT_CHAT",
    "https://t.me/"
)


# =========================================================
# Force Subscribe Configuration
# =========================================================

auth_req_channels = environ.get(
    "AUTH_REQ_CHANNELS",
    ""
)

auth_channels = environ.get(
    "AUTH_CHANNELS",
    ""
)


# =========================================================
# Payment Configuration
# =========================================================

QR_CODE = environ.get(
    "QR_CODE",
    "Your_Qr_Code"
)

OWNER_UPI_ID = environ.get(
    "OWNER_UPI_ID",
    "ɴᴏ ᴀᴠᴀɪʟᴀʙʟᴇ ʀɪɢʜᴛ ɴᴏᴡ"
)

STAR_PREMIUM_PLANS = {
    10: "7day",
    20: "15day",
    40: "1month",
    55: "45day",
    75: "60day",
}


# =========================================================
# MongoDB Configuration
# =========================================================

DATABASE_URI = environ.get(
    "DATABASE_URI",
    "YOUR_MONGODB_URI"
)

DATABASE_NAME = environ.get(
    "DATABASE_NAME",
    "Cluster0"
)

COLLECTION_NAME = environ.get(
    "COLLECTION_NAME",
    "royal_files"
)

MULTIPLE_DB = is_enabled(
    environ.get("MULTIPLE_DB"),
    False
)

DATABASE_URI2 = environ.get(
    "DATABASE_URI2",
    ""
)

if MULTIPLE_DB and not DATABASE_URI2:
    raise ValueError(
        "MULTIPLE_DB=True কিন্তু DATABASE_URI2 দেওয়া হয়নি।"
    )


# =========================================================
# Movie Notification & Update Settings
# =========================================================

MOVIE_UPDATE_NOTIFICATION = is_enabled(
    environ.get("MOVIE_UPDATE_NOTIFICATION"),
    False
)

MOVIE_UPDATE_CHANNEL = int(
    environ.get("MOVIE_UPDATE_CHANNEL", "-100")
)

DREAMXBOTZ_IMAGE_FETCH = is_enabled(
    environ.get("DREAMXBOTZ_IMAGE_FETCH"),
    True
)

LINK_PREVIEW = is_enabled(
    environ.get("LINK_PREVIEW"),
    False
)

ABOVE_PREVIEW = is_enabled(
    environ.get("ABOVE_PREVIEW"),
    True
)

TMDB_API_KEY = environ.get(
    "TMDB_API_KEY",
    ""
)

TMDB_POSTER = is_enabled(
    environ.get("TMDB_POSTER"),
    False
)

LANDSCAPE_POSTER = is_enabled(
    environ.get("LANDSCAPE_POSTER"),
    True
)


# =========================================================
# Verification Settings
# =========================================================

IS_VERIFY = is_enabled(
    environ.get("IS_VERIFY"),
    False
)

LOG_VR_CHANNEL = int(
    environ.get("LOG_VR_CHANNEL", "-100")
)

LOG_API_CHANNEL = int(
    environ.get("LOG_API_CHANNEL", "-100")
)

VERIFY_IMG = environ.get(
    "VERIFY_IMG",
    "https://telegra.ph/file/9ecc5d6e4df5b83424896.jpg"
)

TUTORIAL = environ.get(
    "TUTORIAL",
    "https://t.me/technokrrish"
)

TUTORIAL_2 = environ.get(
    "TUTORIAL_2",
    "https://t.me/technokrrish"
)

TUTORIAL_3 = environ.get(
    "TUTORIAL_3",
    "https://t.me/technokrrish"
)

SHORTENER_API = environ.get(
    "SHORTENER_API",
    ""
)

SHORTENER_WEBSITE = environ.get(
    "SHORTENER_WEBSITE",
    ""
)

SHORTENER_API2 = environ.get(
    "SHORTENER_API2",
    ""
)

SHORTENER_WEBSITE2 = environ.get(
    "SHORTENER_WEBSITE2",
    ""
)

SHORTENER_API3 = environ.get(
    "SHORTENER_API3",
    ""
)

SHORTENER_WEBSITE3 = environ.get(
    "SHORTENER_WEBSITE3",
    ""
)

TWO_VERIFY_GAP = int(
    environ.get("TWO_VERIFY_GAP", "1200")
)

THREE_VERIFY_GAP = int(
    environ.get("THREE_VERIFY_GAP", "54000")
)


# =========================================================
# Channel & Group Links Configuration
# =========================================================

GRP_LNK = environ.get(
    "GRP_LNK",
    "https://t.me/request_gruop"
)

OWNER_LNK = environ.get(
    "OWNER_LNK",
    "https://t.me/request_gruop"
)

UPDATE_CHNL_LNK = environ.get(
    "UPDATE_CHNL_LNK",
    "https://t.me/jacpotfilmm"
)


# =========================================================
# User Configuration
# =========================================================

AUTH_USERS = get_int_list(
    environ.get("AUTH_USERS", "")
)

AUTH_USERS = list(set(AUTH_USERS + ADMINS))

PREMIUM_USER = get_int_list(
    environ.get("PREMIUM_USER", "")
)


# =========================================================
# Miscellaneous Configuration
# =========================================================

ULTRA_FAST_MODE = is_enabled(
    environ.get("ULTRA_FAST_MODE"),
    True
)

MAX_B_TN = int(
    environ.get("MAX_B_TN", "5")
)

PORT = int(
    environ.get("PORT", "8080")
)

MSG_ALRT = environ.get(
    "MSG_ALRT",
    "Share & Support Us ♥️"
)

DELETE_TIME = int(
    environ.get("DELETE_TIME", "300")
)

CUSTOM_FILE_CAPTION = environ.get(
    "CUSTOM_FILE_CAPTION",
    getattr(script, "CAPTION", "")
)

BATCH_FILE_CAPTION = environ.get(
    "BATCH_FILE_CAPTION",
    CUSTOM_FILE_CAPTION
)

IMDB_TEMPLATE = environ.get(
    "IMDB_TEMPLATE",
    getattr(script, "IMDB_TEMPLATE_TXT", "")
)

MAX_LIST_ELM = environ.get(
    "MAX_LIST_ELM",
    None
)

if MAX_LIST_ELM:
    MAX_LIST_ELM = int(MAX_LIST_ELM)

INDEX_REQ_CHANNEL = int(
    environ.get("INDEX_REQ_CHANNEL", str(LOG_CHANNEL))
)

NO_RESULTS_MSG = is_enabled(
    environ.get("NO_RESULTS_MSG"),
    True
)

MAX_BTN = is_enabled(
    environ.get("MAX_BTN"),
    True
)

P_TTI_SHOW_OFF = is_enabled(
    environ.get("P_TTI_SHOW_OFF"),
    False
)

IMDB = is_enabled(
    environ.get("IMDB"),
    False
)

TMDB_ON_SEARCH = is_enabled(
    environ.get("TMDB_ON_SEARCH"),
    False
)

AUTO_FFILTER = is_enabled(
    environ.get("AUTO_FFILTER"),
    True
)

AUTO_DELETE = is_enabled(
    environ.get("AUTO_DELETE"),
    True
)

LONG_IMDB_DESCRIPTION = is_enabled(
    environ.get("LONG_IMDB_DESCRIPTION"),
    False
)

SPELL_CHECK_REPLY = is_enabled(
    environ.get("SPELL_CHECK_REPLY"),
    True
)

MELCOW_NEW_USERS = is_enabled(
    environ.get("MELCOW_NEW_USERS"),
    False
)

PROTECT_CONTENT = is_enabled(
    environ.get("PROTECT_CONTENT"),
    False
)

PM_SEARCH = is_enabled(
    environ.get("PM_SEARCH"),
    True
)

EMOJI_MODE = is_enabled(
    environ.get("EMOJI_MODE"),
    False
)

BUTTON_MODE = is_enabled(
    environ.get("BUTTON_MODE"),
    False
)

STREAM_MODE = is_enabled(
    environ.get("STREAM_MODE"),
    False
)

PREMIUM_STREAM_MODE = is_enabled(
    environ.get("PREMIUM_STREAM_MODE"),
    False
)


# =========================================================
# Bot Configuration
# =========================================================

AUTH_REQ_CHANNELS = get_channel_list(
    auth_req_channels
)

AUTH_CHANNELS = get_channel_list(
    auth_channels
)

REQST_CHANNEL = (
    int(reqst_channel)
    if reqst_channel and id_pattern.fullmatch(reqst_channel)
    else None
)

SUPPORT_CHAT_ID = (
    int(support_chat_id)
    if support_chat_id and id_pattern.fullmatch(support_chat_id)
    else None
)


# =========================================================
# Languages & Qualities
# =========================================================

LANGUAGES = {
    "ᴍᴀʟᴀʏᴀʟᴀᴍ": "mal",
    "ᴛᴀᴍɪʟ": "tam",
    "ᴇɴɢʟɪsʜ": "eng",
    "ʜɪɴᴅɪ": "hin",
    "ʙᴀɴɢʟᴀ": "bengali",
    "ᴛᴇʟᴜɢᴜ": "tel",
    "ᴋᴀɴɴᴀᴅᴀ": "kan",
    "ɢᴜᴊᴀʀᴀᴛɪ": "guj",
    "ᴍᴀʀᴀᴛʜɪ": "mar",
    "ᴘᴜɴᴊᴀʙɪ": "pun",
}

QUALITIES = [
    "360P",
    "480P",
    "720P",
    "1080P",
    "1440P",
    "2160P",
    "4K",
]

SEASON_COUNT = 12

SEASONS = [
    f"S{str(i).zfill(2)}"
    for i in range(1, SEASON_COUNT + 1)
]


# =========================================================
# Bad Words
# =========================================================

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
    "original",
}


# =========================================================
# Server & Web Configuration
# =========================================================

NO_PORT = is_enabled(
    environ.get("NO_PORT"),
    False
)

APP_NAME = environ.get(
    "APP_NAME",
    None
)

ON_HEROKU = "DYNO" in environ

if ON_HEROKU:
    APP_NAME = environ.get("APP_NAME", APP_NAME)

BIND_ADDRESS = environ.get(
    "WEB_SERVER_BIND_ADDRESS",
    "0.0.0.0"
)

FQDN = environ.get(
    "FQDN",
    ""
)

if ON_HEROKU:
    FQDN = FQDN or (
        f"{APP_NAME}.herokuapp.com"
        if APP_NAME
        else "localhost"
    )
else:
    FQDN = FQDN or "localhost"

HAS_SSL = is_enabled(
    environ.get("HAS_SSL"),
    True
)

if HAS_SSL:
    URL = f"https://{FQDN}/"
else:
    URL = f"http://{FQDN}/"

if not ON_HEROKU and not NO_PORT:
    URL = f"{'https' if HAS_SSL else 'http'}://{FQDN}:{PORT}/"

SLEEP_THRESHOLD = int(
    environ.get("SLEEP_THRESHOLD", "60")
)

WORKERS = int(
    environ.get("WORKERS", "4")
)

SESSION_NAME = environ.get(
    "SESSION_NAME",
    "dreamXBotz"
)

MULTI_CLIENT = is_enabled(
    environ.get("MULTI_CLIENT"),
    False
)

name = environ.get(
    "name",
    "DREAMXBOTZ"
)

PING_INTERVAL = int(
    environ.get("PING_INTERVAL", "1200")
)


# =========================================================
# Reactions Configuration
# =========================================================

REACTIONS = [
    "🤝", "😇", "🤗", "😍", "👍", "🎅", "😐",
    "🥰", "🤩", "😱", "🤣", "😘", "👏", "😛",
    "😈", "🎉", "⚡️", "🫡", "🤓", "😎",
    "🏆", "🔥", "🤭", "🌚", "🆒", "👻", "😁"
]


# =========================================================
# Bot Commands
# =========================================================

Bot_cmds = {
    "start": "Sᴛᴀʀᴛ Mᴇ Bᴀʙʏ",
    "stats": "Gᴇᴛ Bᴏᴛ Sᴛᴀᴛs",
    "alive": "Cʜᴇᴄᴋ Bᴏᴛ Aʟɪᴠᴇ ᴏʀ Nᴏᴛ",
    "settings": "ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs",
    "id": "ɢᴇᴛ ɪᴅ ᴛᴇʟᴇɢʀᴀᴍ",
    "info": "Gᴇᴛ Usᴇʀ Iɴғᴏ",
    "del_msg": "ʀᴇᴍᴏᴠᴇ ғɪʟᴇ ɴᴀᴍᴇ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ",
    "movie_update": "ᴏɴ ᴏғғ ᴀᴄᴄᴏʀᴅɪɴɢ ʏᴏᴜʀ ɴᴇᴇᴅᴇᴅ",
    "pm_search": "ᴘᴍ sᴇᴀʀᴄʜ ᴏɴ ᴏғғ",
    "trendlist": "Gᴇᴛ Tᴏᴘ Tʀᴇɴᴅɪɴɢ Sᴇᴀʀᴄʜ Lɪsᴛ",
    "broadcast": "Bʀᴏᴀᴅᴄᴀsᴛ ᴀ Mᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ Usᴇʀs",
    "grp_broadcast": "Bʀᴏᴀᴅᴄᴀsᴛ ᴛᴏ ᴀʟʟ Cᴏɴɴᴇᴄᴛᴇᴅ Gʀᴏᴜᴘs",
    "send": "Sᴇɴᴅ Mᴇssᴀɢᴇ ᴛᴏ ᴀ Pᴀʀᴛɪᴄᴜʟᴀʀ Usᴇʀ",
    "add_premium": "Aᴅᴅ Usᴇʀ ᴛᴏ Pʀᴇᴍɪᴜᴍ",
    "remove_premium": "Rᴇᴍᴏᴠᴇ Usᴇʀ ғʀᴏᴍ Pʀᴇᴍɪᴜᴍ",
    "premium_users": "Gᴇᴛ Pʀᴇᴍɪᴜᴍ Usᴇʀs",
    "restart": "Rᴇsᴛᴀʀᴛ Tʜᴇ Bᴏᴛ",
    "group_cmd": "Gʀᴏᴜᴘ Cᴏᴍᴍᴀɴᴅ Lɪsᴛ",
    "admin_cmd": "Aᴅᴍɪɴ Cᴏᴍᴍᴀɴᴅs Lɪsᴛ",
    "reset_group": "Gʀᴏᴜᴘ Sᴇᴛᴛɪɴɢ Dᴇғᴀᴜʟᴛ",
    "trial_reset": "Usᴇʀ Tʀɪᴀʟ Rᴇsᴇᴛ",
}


# =========================================================
# Final Database Configuration
# =========================================================

if not MULTIPLE_DB:
    DATABASE_URI2 = DATABASE_URI


# =========================================================
# Logs Configuration
# =========================================================

LOG_STR = "Current Customized Configurations are:\n"

LOG_STR += (
    "IMDB Results are enabled.\n"
    if IMDB
    else "IMDB Results are disabled.\n"
)

LOG_STR += (
    "P_TTI_SHOW_OFF is enabled.\n"
    if P_TTI_SHOW_OFF
    else "P_TTI_SHOW_OFF is disabled.\n"
)

LOG_STR += (
    "BUTTON_MODE is enabled.\n"
    if BUTTON_MODE
    else "BUTTON_MODE is disabled.\n"
)

LOG_STR += (
    f"CUSTOM_FILE_CAPTION enabled: {CUSTOM_FILE_CAPTION}\n"
    if CUSTOM_FILE_CAPTION
    else "Default file caption will be used.\n"
)

LOG_STR += (
    "Long IMDB description is enabled.\n"
    if LONG_IMDB_DESCRIPTION
    else "Long IMDB description is disabled.\n"
)

LOG_STR += (
    "Spell Check Mode is enabled.\n"
    if SPELL_CHECK_REPLY
    else "Spell Check Mode is disabled.\n"
)
