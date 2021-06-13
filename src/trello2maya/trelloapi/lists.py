"""
Provides communication with Trello REST API for List information
"""

from json import loads
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from .config import API_KEY, LISTS_URL

def get(token, list_id):
    params = {
        'key': API_KEY,
        'token': token }

    request = Request(f'{LISTS_URL}{list_id}?{urlencode(params)}')

    with urlopen(request) as response:
        return loads(response.read())

def create(token, list_name, board_id):
    params = {
        'key': API_KEY,
        'token': token,
        'name': list_name,
        'idBoard': board_id,
        'pos': 'bottom' }

    request = Request(f'{LISTS_URL}?{urlencode(params)}', method='POST')

    with urlopen(request) as response:
        return loads(response.read())

def update(token, list_id, list_name, board_id):
    params = {
        'key': API_KEY,
        'token': token,
        'name': list_name,
        'idBoard': board_id }

    request = Request(f'{LISTS_URL}{list_id}?{urlencode(params)}', method='PUT')

    with urlopen(request) as response:
        return loads(response.read())

def delete(token, list_id):
    params = {
        'key': API_KEY,
        'token': token }
    request = Request(f'{LISTS_URL}{list_id}?{urlencode(params)}', method='DELETE')

    with urlopen(request) as response:
        return loads(response.read())

def archive(token, list_id):
    params = {
        'key': API_KEY,
        'token': token,
        'value': 'true' }

    request = Request(f'{LISTS_URL}{list_id}/closed?{urlencode(params)}', method='PUT')

    with urlopen(request) as response:
        return loads(response.read())

def list_cards(token, list_id):
    params = {
        'key': API_KEY,
        'token': token,
        'value': 'true' }

    request = Request(f'{LISTS_URL}{list_id}/cards?{urlencode(params)}')

    with urlopen(request) as response:
        return loads(response.read())
