# Created By @DaRrKNneSs_1&@R7_OX
# Copyright By SIMO&ROWES

from os import getenv

from dotenv import load_dotenv

load_dotenv()

que = {}
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
BOT_NAME = getenv("BOT_NAME", "")
BOT_USERNAME = getenv("BOT_USERNAME", "")
ASSID = int(getenv("ASSID", ""))
ASSNAME = getenv("ASSNAME", "")
ASSUSERNAME = getenv("ASSUSERNAME", "")

BOT_ID = int(getenv("BOT_ID", ""))
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
MONGO_DB_URI = getenv("MONGO_DB_URI", "")
API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH", "")
OWNER_ID = int(getenv("OWNER_ID", ""))
UPDATE = getenv("UPDATE", "")
SUPPORT = getenv("SUPPORT", "")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "999"))
CMD_MUSIC = list(getenv("CMD_MUSIC", ". / ! + - @ # $").split())
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", "")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split()))
START_PIC = getenv("START_PIC", "https://graph.org/file/15dd5ca3978e826ffc726.jpg")
OWNER_USERNAME = getenv("OWNER_USERNAME", "")
IMG_1 = getenv("IMG_1", "https://graph.org/file/ab6b8fa496fd7d8f75b0e.jpg")
IMG_2 = getenv("IMG_2", "https://graph.org/file/ab6b8fa496fd7d8f75b0e.jpg")
IMG_3 = getenv("IMG_3", "https://graph.org/file/ab6b8fa496fd7d8f75b0e.jpg")
IMG_4 = getenv("IMG_4", "https://graph.org/file/ab6b8fa496fd7d8f75b0e.jpg")
