"""
Provides logic and user interface for managing Trello2Maya configuration and authorization
"""

import maya.cmds as cmds
from .trelloapi.auth import request_token
from .trelloapi.members import list_boards
from .util import command_wrapper, load_token, save_token

MARGIN_SIZE = 5
CONTROL_HEIGHT = 25
BUTTON_WIDTH = 125
TOKEN_FIELD_KEY = 'token_field'

def authorize_api():
    request_token()

def test_token(token_field):
    api_token = cmds.textField(token_field, query=True, text=True)

    try:
        list_boards(api_token)
    except:
        cmds.confirmDialog(
            message='Token is not authorized. Please click on Authorize button to generate token.',
            title='Invalid',
            icon='critical')
    else:
        cmds.confirmDialog(
            message='Token is authorized. Please click on Save button to store authorized token.',
            title='Valid',
            icon='information')

def config_window():
    ui_title = 'trello2maya_options'

    if cmds.window(ui_title, exists=True):
        cmds.deleteUI(ui_title, window=True)

    window = cmds.window(
        ui_title,
        title='Trello2Maya Options',
        sizeable=False,
        maximizeButton=False,
        minimizeButton=False)

    root_layout = cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)

    cmds.separator(width=MARGIN_SIZE, style='none')

    inner_layout = cmds.columnLayout(adjustableColumn=True)

    token_fields = token_info(inner_layout)

    cmds.separator(height=MARGIN_SIZE, style='none')

    command_buttons(inner_layout, token_fields[TOKEN_FIELD_KEY])

    cmds.separator(height=MARGIN_SIZE, style='none')
    cmds.setParent(root_layout)
    cmds.separator(width=MARGIN_SIZE, style='none')


    cmds.showWindow(window)

def token_info(parent):
    cmds.setParent(parent)

    cmds.text('Trello API Token', height=CONTROL_HEIGHT, font='boldLabelFont')

    token_field = cmds.textField(
        text=load_token(),
        height=CONTROL_HEIGHT,
        placeholderText='API Token from Trello.com')

    cmds.setParent(parent)

    return { TOKEN_FIELD_KEY: token_field }


def command_buttons(parent, token_field):
    cmds.setParent(parent)

    cmds.rowLayout(numberOfColumns=5)
    cmds.button(
        'Authorize',
        command=command_wrapper(request_token),
        width=BUTTON_WIDTH,
        height=CONTROL_HEIGHT)
    cmds.separator(width=MARGIN_SIZE, style='none')
    cmds.button(
        'Test',
        command=command_wrapper(test_token, token_field),
        width=BUTTON_WIDTH,
        height=CONTROL_HEIGHT)
    cmds.separator(width=MARGIN_SIZE, style='none')
    cmds.button(
        'Save',
        command=command_wrapper(save_token, token_field),
        width=BUTTON_WIDTH,
        height=CONTROL_HEIGHT)

    cmds.setParent(parent)
