from os import environ

from src.config.logs import setup_logging
from src.config.settings.base import *  # noqa

setup_logging(enable_json=True)

SECRET_KEY = environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "").split(",")
