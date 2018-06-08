import requests
import time
from flask import Blueprint, render_template

from app.constants import (
    DISCORD_API, DISCORD_CLIENT_ID, DISCORD_SECRET
)

main_bp = Blueprint("main", __name__)
current_token = {}


def get_access_token():
    """
    Get an access token for my Discord user. This is used to grant
    access to information for identifying my user, such as my username
    or my discriminator.
    """

    url = "{}/oauth2/token".format(DISCORD_API)

    # 'client_credentials' is a special grant type which allows us to
    # get data about my user without needing to provide a redirect URI
    data = {
        "grant_type": "client_credentials",
        "scope": "identify"
    }

    # Discord API OAuth2 Documentation:
    #     "In accordance with RFC 6749, the token URL only
    #      accepts a content type of x-www-form-urlencoded"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Get our token information from Discord.
    response = requests.post(
        url,
        data=data,
        headers=headers,
        auth=(DISCORD_CLIENT_ID, DISCORD_SECRET)
    )

    as_json = response.json()

    # Add a new value to specify the time at which the access token expires.
    as_json["expire_time"] = time.time() + as_json["expires_in"]

    return as_json


def get_user_info(token):
    """Use a Discord API OAuth2 access token to retrieve information about my user."""
    url = "{}/users/@me".format(DISCORD_API)

    # The Discord API requires a very specific format for the Authorization header.
    # In our case, it would follow the format of:
    #     "Authorization: TOKEN_TYPE TOKEN"
    headers = {
        "User-Agent": "Contact Updater (for https://www.codingbykingsley.co.uk/)",
        "Authorization": "{token[token_type]} {token[access_token]}".format(token=token)
    }

    response = requests.get(
        url,
        headers=headers
    )

    return response.json()


@main_bp.route("/")
def index():
    # We only need to update the token if it's empty or has expired. 
    if not current_token or current_token["expire_time"] < time.time():
        # Really hacky way of modifying current_token in-place
        # rather than declaring it as a global variable :I
        new_token = get_access_token()
        current_token.update(new_token)

    user_info = get_user_info(current_token)
    return render_template("main/index.html", user=user_info)