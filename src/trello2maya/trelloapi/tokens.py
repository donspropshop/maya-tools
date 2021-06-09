"""
Provides communication with Trello REST API for Token information
"""

from json import loads
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from .config import API_KEY, TOKENS_URL

def get(token):
    params = { 'key': API_KEY }

    request = Request(f'{TOKENS_URL}{token}?{urlencode(params)}')

    with urlopen(request) as response:
        return loads(response.read())

def get_member(token):
    params = { 'key': API_KEY,'token': token }

    request = Request(f'{TOKENS_URL}{token}/member?{urlencode(params)}')

    with urlopen(request) as response:
        return loads(response.read())
