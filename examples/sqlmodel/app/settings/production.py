from pathlib import Path

DEBUG = True
MEDIA_ROOT = "assets"
MEDIA_PATH = Path(__file__).resolve().parent / MEDIA_ROOT
PLUGINS = [
    # "fastack.plugins.aioredis",
    "fastack.plugins.sqlmodel",
    # "fastack.plugins.mongoengine",
]
COMMANDS = [
    # "app.commands.user.cli"
]

# if you use the ``fastack.plugins.sqlmodel``` plugin.
# ----------------------------------------------------
DB_USER = "fastack_user"
DB_PASSWORD = "fastack_pass"
DB_HOST = "db"
DB_PORT = 5432
DB_NAME = "fastack_db"
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
SQLALCHEMY_CONNECT_ARGS = {}
SQLALCHEMY_OPTIONS = {"echo": True}

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
