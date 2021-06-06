"""
Add a random affirmation from affirmations.dev to Maya

Usage:
- Place affirmation.py in your Maya user scripts folder
- Add the following Python to a custom shelf button

import affirmation
affirmation.affirm()
"""

import maya.cmds as cmds
import json
import urllib.request

def affirm():
    with urllib.request.urlopen('https://affirmations.dev') as response:
        data = json.loads(response.read())
        cmds.confirmDialog(title='Affirmation', message=data['affirmation'])