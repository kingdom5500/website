import os


# Used to configure the actual application
class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    SERVER_NAME = "codingbykingsley.co.uk"


# Constants for the SQLite database.
DATABASE = "app/database.db"
DATABASE_SCHEMA = "app/schema.sql"

# These are for getting my Discord user
# information via the official API. 
DISCORD_API = "https://discordapp.com/api"
DISCORD_CLIENT_ID = "452303710715117578"
DISCORD_SECRET = os.environ["DISCORD_SECRET"]
