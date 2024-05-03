from src.config.settings.base import *  # noqa

from src.config.logs import setup_logging

setup_logging(enable_json=True)

SECRET_KEY = "###local secret###"  # noqa:S105

DEBUG = True

ALLOWED_HOSTS = ["*"]
