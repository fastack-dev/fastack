DEBUG = True
PLUGINS = [
    "fastack_sqlmodel",
    "fastack_migrate",
]

COMMANDS = []

DB_USER = ""
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = 5888
DB_NAME = ""
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
SQLALCHEMY_OPTIONS = {"echo": True}
