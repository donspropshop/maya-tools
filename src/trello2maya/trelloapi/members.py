"""
Provides communication with Trello REST API for Member information
"""

from json import loads
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from .config import API_KEY, MEMBERS_URL

def get(token, member_id='me'):
    params = {
        'key': API_KEY,
        'token': token }

    request = Request(f'{MEMBERS_URL}{member_id}?{urlencode(params)}')

    with urlopen(request) as response:
        return loads(response.read())

def list_boards(token, member_id='me'):
    params = {
        'key': API_KEY,
        'token': token }

    request = Request(f'{MEMBERS_URL}{member_id}/boards?{urlencode(params)}')

    with urlopen(request) as response:
        return loads(response.read())
