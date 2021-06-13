"""
Provides communication with Trello for user authorization of application
"""

from webbrowser import open as open_browser
from .config import AUTH_URL, API_KEY, APP_NAME, APP_SCOPE, TOKEN_EXPIRY

def request_token():
    auth_url = AUTH_URL + '?key={}&name={}&scope={}&expiration={}&response_type=token'
    open_browser(auth_url.format(API_KEY, APP_NAME, APP_SCOPE, TOKEN_EXPIRY))
