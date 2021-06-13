"""
Provides communication with Trello REST API for Card information
"""

from json import loads
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from .config import API_KEY, CARDS_URL

def get(token, card_id):
    params = {
        'key': API_KEY,
        'token': token }

    request = Request(f'{CARDS_URL}{card_id}?{urlencode(params)}')

    with urlopen(request) as response:
        return loads(response.read())

def create(token, card_name, card_description, list_id):
    params = {
        'key': API_KEY,
        'token': token,
        'name': card_name,
        'desc': card_description,
        'idList': list_id,
        'pos': 'bottom' }

    request = Request(f'{CARDS_URL}?{urlencode(params)}', method='POST')

    with urlopen(request) as response:
        return loads(response.read())

def update(token, card_id, card_name, card_description):
    params = {
        'key': API_KEY,
        'token': token,
        'name': card_name,
        'desc': card_description }

    request = Request(f'{CARDS_URL}{card_id}?{urlencode(params)}', method='PUT')

    with urlopen(request) as response:
        return loads(response.read())

def delete(token, card_id):
    params = {
        'key': API_KEY,
        'token': token}

    request = Request(f'{CARDS_URL}{card_id}?{urlencode(params)}', method='DELETE')

    with urlopen(request) as response:
        return loads(response.read())

def move(token, card_id, list_id):
    params = {
        'key': API_KEY,
        'token': token,
        'idList': list_id }

    request = Request(f'{CARDS_URL}{card_id}?{urlencode(params)}', method='PUT')

    with urlopen(request) as response:
        return loads(response.read())

def add_comment(token, card_id, comment):
    params = {
        'key': API_KEY,
        'token': token,
        'text': comment }

    request = Request(f'{CARDS_URL}{card_id}/actions/comments?{urlencode(params)}', method='POST')

    with urlopen(request) as response:
        return loads(response.read())
