import environ

##################################################################
# explicitly load .env file. so there are the same ENV variables
# as when using direnv.
# this also works for pycharm / vs-code run configurations.
# https://direnv.net/
##################################################################
env = environ.Env()
env.read_env(env.str("ENV_PATH", ".env"))

from .base import *  # NOQA

# from .gcp_logging import LOGGING  # NOQA
from .dev_logging import LOGGING  # NOQA
from .development import *  # NOQA

##################################################################
# make sure to add further setting overrides *after*
# importing .development
##################################################################

# from django.conf import settings
#
# print("DEBUG", settings.DEBUG)
# print("DATABASES", settings.DATABASES)
# print("EMAIL_BACKEND", settings.EMAIL_BACKEND)
