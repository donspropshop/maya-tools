"""
Provides communication with Trello REST API for Board information
"""

from json import loads
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from .config import API_KEY, BOARDS_URL

def get(token, board_id):
    params = {
        'key': API_KEY,
        'token': token}

    request = Request(f'{BOARDS_URL}{board_id}?{urlencode(params)}')

    with urlopen(request) as response:
        return loads(response.read())

def create(token, board_name, board_description):
    params = {
        'key': API_KEY,
        'token': token,
        'name': board_name,
        'desc': board_description }

    request = Request(f'{BOARDS_URL}?{urlencode(params)}', method='POST')

    with urlopen(request) as response:
        return loads(response.read())

def update(token, board_id, board_name, board_description):
    params = {
        'key': API_KEY,
        'token': token,
        'name': board_name,
        'desc': board_description }

    request = Request(f'{BOARDS_URL}{board_id}?{urlencode(params)}', method='PUT')

    with urlopen(request) as response:
        return loads(response.read())

def delete(token, board_id):
    params = {
        'key': API_KEY,
        'token': token }

    request = Request(f'{BOARDS_URL}{board_id}?{urlencode(params)}', method='DELETE')

    with urlopen(request) as response:
        return loads(response.read())

def close(token, board_id):
    params = {
        'key': API_KEY,
        'token': token,
        'closed': 'true' }

    request = Request(f'{BOARDS_URL}{board_id}?{urlencode(params)}', method='PUT')

    with urlopen(request) as response:
        return loads(response.read())

def list_lists(token, board_id):
    params = {
        'key': API_KEY,
        'token': token }

    request = Request(f'{BOARDS_URL}{board_id}/lists?{urlencode(params)}')

    with urlopen(request) as response:
        return loads(response.read())

def list_cards(token, board_id):
    params = {
        'key': API_KEY,
        'token': token }

    request = Request(f'{BOARDS_URL}{board_id}/cards?{urlencode(params)}')

    with urlopen(request) as response:
        return loads(response.read())
