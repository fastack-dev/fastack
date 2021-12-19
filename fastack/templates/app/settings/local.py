from pathlib import Path

DEBUG = True
MEDIA_ROOT = "assets"
MEDIA_PATH = Path(__file__).resolve().parent / MEDIA_ROOT
PLUGINS = [
    # "fastack.plugins.aioredis",
    # "fastack.plugins.sqlmodel",
    # "fastack.plugins.mongoengine",
]
COMMANDS = [
    # "app.commands.user.cli"
]

# if you use the ``fastack.plugins.sqlmodel``` plugin.
# ----------------------------------------------------
# SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
# SQLALCHEMY_CONNECT_ARGS = {"check_same_thread": False}
# SQLALCHEMY_OPTIONS = {"echo": True}

# if you use the ``fastack.plugins.mongoengine``` plugin.
# -------------------------------------------------------
# MONGODB_NAME = ""
# MONGODB_USER = ""
# MONGODB_PASSWORD = ""
# MONGODB_HOST = ""
# MONGODB_PORT = 27017
# MONGODB_URI = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}/{MONGODB_NAME}"

# if you use the ``fastack.plugins.aioredis``` plugin.
# ----------------------------------------------------
# REDIS_HOST = "localhost"
# REDIS_PORT = 6379
# REDIS_DB = 0
# REDIS_PASSWORD = None
# CACHES = {
#     "default": {
#         "host": REDIS_HOST,
#         "port": REDIS_PORT,
#         "db": REDIS_DB,
#         "password": REDIS_PASSWORD,
#     }
# }
