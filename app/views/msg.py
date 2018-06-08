import sqlite3
from datetime import datetime

from flask import Blueprint, render_template, request, g, redirect, url_for

from app import limiter
from app.constants import DATABASE
from app.forms import PostForm

msg_bp = Blueprint("msg", __name__, subdomain="msg")


def get_db():
    """Get the current database connection, or create a new one if one doesn't exist"""
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    return db


# Create a new list of messages. Will be updated automatically.
messages = []


@msg_bp.route("/", methods=["GET", "POST"])
@limiter.limit("3 per minute", methods=["POST"])
def index():
    """The main 'msg' index, where a visitor may view or post a message."""
    db = get_db()
    cur = db.cursor()
    form = PostForm()

    # We only want to add to the database if the entry passed validation checks.
    if form.validate_on_submit():

        data = (
            request.form["name"].strip() or "Anonymous",
            request.form["message"],
            str(datetime.now()),
        )

        # Insert the generated data into the table.
        cur.execute("INSERT INTO messages(name, message, created) VALUES (?, ?, ?)", data)
        db.commit()

        # Add the row-id to the data so we can cache it properly.
        data["id"] = cur.lastrowid

        # Finally, add the data to our cache so we don't kill the database on every request
        messages.append(data)

        return redirect(url_for("msg.index"))

    # Load the messages if they haven't been cached yet.
    if not messages:
        cur.execute("SELECT * FROM messages")
        messages.extend(cur.fetchall())

    return render_template('msg/index.html', form=form, posts=reversed(messages), admin=False)


@msg_bp.route("/admin", methods=["GET", "POST"])
def admin():
    """Just a simple admin panel for deleting messages and stuff like that."""
    db = get_db()
    cur = db.cursor()
    
    if request.method == "POST":
        try:
            target = request.form["delete"]
        except KeyError:
            pass
        else:
            cur.execute("DELETE FROM messages WHERE id = ?", (target,))
            db.commit()

    # Load the messages if they haven't been cached yet.
    if not messages:
        cur.execute("SELECT * FROM messages")
        messages.extend(cur.fetchall())

    return render_template('msg/title.html', posts=reversed(messages), admin=True)


@msg_bp.route("/message-<int:msg_id>")
def message(msg_id: int):
    """Permalinks of individual messages are managed here."""
    db = get_db()
    cur = db.cursor()
    
    # Get all details of the specified message from the database.
    cur.execute("SELECT * FROM messages WHERE id = ?", (msg_id,))
    msg = cur.fetchone()
    
    # If a message was found, send the template out.
    if msg is not None:
        return render_template('msg/message.html', msg=msg)
    # If the message could not be found, redirect to the main index.
    else:
        return redirect(url_for("msg.index"))
  