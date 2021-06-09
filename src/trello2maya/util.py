"""
Provides shared utility functions
"""
import maya.cmds as cmds

API_TOKEN_SETTING = 'trelloApiToken'
SHELF_NAME = 'Trello2Maya'

def setup_shelf():
    if cmds.shelfLayout(SHELF_NAME, exists=True):
        cmds.deleteUI(SHELF_NAME)

    cmds.shelfLayout(SHELF_NAME, parent="ShelfLayout", spacing=20)

    cmds.shelfButton(
        'T2M Main',
        parent=SHELF_NAME,
        annotation='T2M Main App',
        label='Trello',
        image='menuIconList.png',
        sourceType='Python',
        command='import trello2maya.main as tmm; tmm.launcher()')

    cmds.shelfButton(
        'T2M Config',
        parent=SHELF_NAME,
        annotation='T2M Config',
        label='Config',
        image='hotkeySetSettings.png',
        sourceType='Python',
        command='import trello2maya.config as tmc; tmc.config_window()')

def command_wrapper(func, *args, **kwargs):
    def wrapped(*_):
        func(*args, **kwargs)

    return wrapped

def save_token(token_field):
    api_token = cmds.textField(token_field, query=True, text=True)
    cmds.optionVar(stringValue=(API_TOKEN_SETTING, api_token))

def load_token():
    if not cmds.optionVar(exists=API_TOKEN_SETTING):
        return ''

    return cmds.optionVar(query=API_TOKEN_SETTING)
