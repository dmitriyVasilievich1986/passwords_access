from os import getenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = str(getenv("DEBUG")).lower() == "true"

PASSWORD = getenv("PASSWORD")
USERNAME = getenv("USERNAME")
HOST = getenv("HOST")
PORT = getenv("PORT")

LOGIN_URL = "/login"
LOGOUT_URL = "/logout"
PASSWORDS_API = "/api/v1/password"
