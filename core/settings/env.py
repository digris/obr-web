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
from .development import *  # NOQA

# from .dev_logging import LOGGING  # NOQA

##################################################################
# make sure to add further setting overrides *after*
# importing .development
##################################################################

MIDDLEWARE += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # "querycount.middleware.QueryCountMiddleware",
]

# DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
# GS_BUCKET_NAME = "ch-openbroadcast-media"
# GS_DEFAULT_ACL = "publicRead"
