from os import environ, getenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = str(getenv("DEBUG")).lower() == "true"

PASSWORD = environ["AUTH_PASSWORD"]
USERNAME = environ["AUTH_USERNAME"]
PORT = int(environ["AUTH_PORT"])
HOST = environ["AUTH_HOST"]

LOGIN_URL = "/login"
LOGOUT_URL = "/logout"
PASSWORDS_API = "/api/v1/password"
