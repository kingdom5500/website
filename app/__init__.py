import sqlite3

from flask import Flask, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.constants import DATABASE, DATABASE_SCHEMA

app = Flask(__name__)
app.config.from_object("app.constants.Config")


def init_database():
    """
    Simply for initialising the database on start-up. This
    will execute the schematic to define the default tables
    """
    db = sqlite3.connect(DATABASE)

    with open(DATABASE_SCHEMA) as schema:
        db.executescript(schema.read())
        db.commit()
    
    db.close()


init_database()


@app.teardown_appcontext
def close_connection(exception):
    """Automatically close the database connection once a request is finished."""
    db = getattr(g, '_database', None)
    
    if db is not None:
        db.close()


# This is used to apply rate-limits on various views
limiter = Limiter(
    app,
    key_func=get_remote_address
)

# These imports are here to avoid circular import errors
from app.views.main import main_bp
from app.views.msg import msg_bp

app.register_blueprint(main_bp)
app.register_blueprint(msg_bp)
