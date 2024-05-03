from os import environ

from src.config.settings.base import *  # noqa

SECRET_KEY = environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "").split(",")
