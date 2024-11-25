from os import environ, getenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = str(getenv("DEBUG")).lower() == "true"

PASSWORD = environ["PASSWORD"]
USERNAME = environ["USERNAME"]
PORT = int(environ["PORT"])
HOST = environ["HOST"]

LOGIN_URL = "/login"
LOGOUT_URL = "/logout"
PASSWORDS_API = "/api/v1/password"
