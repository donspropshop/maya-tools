"""
Main application logic and user interface
"""

import maya.cmds as cmds
from .config import config_window
from .trelloapi import members, boards, lists, cards
from .util import load_token, command_wrapper

MARGIN_SIZE = 5
CONTROL_HEIGHT = 25
TITLE_KEY = 'text_title'
LIST_KEY = 'scroll_list'
CREATE_KEY = 'icon_create'
DELETE_KEY = 'icon_delete'
RELOAD_KEY = 'icon_reload'
CARD_DETAILS_KEY = 'card_details'

API_TOKEN = load_token()

def launcher():
    if not test_token():
        config_window()
        cmds.confirmDialog(
            message='Token is not authorized. Please click on Authorize button to generate token.',
            title='Invalid',
            icon='critical')
        return

    main_window()

def test_token():
    try:
        members.list_boards(API_TOKEN)
        return True
    except:
        return None

def load_boards(boards_ui, lists_ui, cards_ui, card_details_ui):
    member_info = members.get(API_TOKEN)

    clear_items_ui(f"{member_info['fullName']}'s Boards", boards_ui)
    clear_items_ui('Board Lists', lists_ui)
    clear_items_ui('List Cards', cards_ui)
    clear_detail_ui(card_details_ui)

    trello_boards = members.list_boards(API_TOKEN)
    active_boards = [board for board in trello_boards if not board['closed']]

    if active_boards:
        board_names = [board['name'] for board in active_boards]
        board_keys = [board['id'] for board in active_boards]

        cmds.textScrollList(
            boards_ui[LIST_KEY],
            edit=True,
            append=board_names,
            uniqueTag=board_keys)

def load_lists(boards_ui, lists_ui, cards_ui, card_details_ui):
    clear_items_ui('Board Lists', lists_ui)
    clear_items_ui('List Cards', cards_ui)
    clear_detail_ui(card_details_ui)

    selected_board_ids = cmds.textScrollList(
        boards_ui[LIST_KEY],
        query=True,
        selectUniqueTagItem=True)

    if not selected_board_ids:
        return

    selected_board_names = cmds.textScrollList(boards_ui[LIST_KEY], query=True, selectItem=True)
    list_info = boards.list_lists(API_TOKEN, selected_board_ids[0])

    list_names = [list['name'] for list in list_info]
    list_keys = [list['id'] for list in list_info]

    cmds.text(lists_ui[TITLE_KEY], edit=True, label=f'{selected_board_names[0]} Lists')
    cmds.textScrollList(lists_ui[LIST_KEY], edit=True, append=list_names, uniqueTag=list_keys)

def load_cards(lists_ui, cards_ui, card_details_ui):
    clear_items_ui('List Cards', cards_ui)
    clear_detail_ui(card_details_ui)
    selected_list_ids = cmds.textScrollList(
        lists_ui[LIST_KEY],
        query=True,
        selectUniqueTagItem=True)

    if not selected_list_ids:
        return

    selected_list_names = cmds.textScrollList(lists_ui[LIST_KEY], query=True, selectItem=True)
    card_info = lists.list_cards(API_TOKEN, selected_list_ids[0])

    card_names = [card['name'] for card in card_info]
    card_keys = [card['id'] for card in card_info]

    cmds.text(cards_ui[TITLE_KEY], edit=True, label=f'{selected_list_names[0]} Cards')
    cmds.textScrollList(cards_ui[LIST_KEY], edit=True, append=card_names, uniqueTag=card_keys)

def load_card(boards_ui, lists_ui, cards_ui, card_details_ui):
    clear_detail_ui(card_details_ui)
    selected_card_ids = cmds.textScrollList(
        cards_ui[LIST_KEY],
        query=True,
        selectUniqueTagItem=True)

    if not selected_card_ids:
        return

    card_info = cards.get(API_TOKEN, selected_card_ids[0])

    cmds.setParent(card_details_ui[CARD_DETAILS_KEY])
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(
        label='Name',
        height=CONTROL_HEIGHT,
        font='boldLabelFont',
        align='left')

    card_name = cmds.textField(
        text=card_info['name'],
        height=CONTROL_HEIGHT)

    cmds.setParent(card_details_ui[CARD_DETAILS_KEY])
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(
        label='Description',
        height=CONTROL_HEIGHT,
        font='boldLabelFont',
        align='left')

    card_desc = cmds.scrollField(
        text=card_info['desc'],
        height=CONTROL_HEIGHT*4,
        wordWrap=True)

    cmds.setParent(card_details_ui[CARD_DETAILS_KEY])
    button_panel = cmds.rowLayout(
        numberOfColumns=2,
        adjustableColumn=1,
        columnAlign=[2,'right'],
        columnAttach=[2,'left', 5])

    board_id = cmds.textScrollList(boards_ui[LIST_KEY], query=True, selectUniqueTagItem=True)[0]
    lists_info = boards.list_lists(API_TOKEN, board_id)
    cmds.flowLayout(
        wrap=False,
        columnSpacing=MARGIN_SIZE*2,
        width=(CONTROL_HEIGHT*3 + MARGIN_SIZE*2)*len(lists_info))

    for list_info in lists_info:
        button = cmds.button(
            label=list_info['name'],
            height=CONTROL_HEIGHT,
            width=CONTROL_HEIGHT*3)

        if card_info['idList'] == list_info['id']:
            cmds.button(button, edit=True, enable=False)
        else:
            cmds.button(
                button,
                edit=True,
                command=command_wrapper(
                    send_to_list,
                    boards_ui,
                    lists_ui,
                    cards_ui,
                    card_details_ui,
                    card_info['id'],
                    list_info['id']))

    cmds.setParent(button_panel)
    cmds.button(
        label='Save',
        height=CONTROL_HEIGHT,
        width=CONTROL_HEIGHT*3,
        command=command_wrapper(
            save_card,
            boards_ui,
            lists_ui,
            cards_ui,
            card_details_ui,
            card_info['id'],
            card_name,
            card_desc))

    cmds.setParent(card_details_ui[CARD_DETAILS_KEY])

def clear_items_ui(title_text, layout_ui):
    cmds.text(layout_ui[TITLE_KEY], edit=True, label=title_text)
    cmds.textScrollList(layout_ui[LIST_KEY], edit=True, removeAll=True)

def clear_detail_ui(detail_ui):
    children = cmds.columnLayout(detail_ui[CARD_DETAILS_KEY], query=True, childArray=True)

    if not children:
        return

    for child in children:
        cmds.deleteUI(child)

def add_board(boards_ui, lists_ui, cards_ui, card_details_ui):
    result = cmds.promptDialog(
        title='Create new board.',
        message='Board name:',
        dismissString = '',
        button='Create')

    if result == 'Create':
        new_board_name = cmds.promptDialog(query=True, text=True).strip()

        if new_board_name:
            boards.create(API_TOKEN, new_board_name, '')

    reload_boards(boards_ui, lists_ui, cards_ui, card_details_ui)

def close_board(boards_ui, lists_ui, cards_ui, card_details_ui):
    board_ids = cmds.textScrollList(boards_ui[LIST_KEY], query=True, selectUniqueTagItem=True)

    if board_ids:
        boards.close(API_TOKEN, board_ids[0])
        cmds.textScrollList( boards_ui[LIST_KEY], edit=True, removeAll=True)
        reload_boards(boards_ui, lists_ui, cards_ui, card_details_ui)

def reload_boards(boards_ui, lists_ui, cards_ui, card_details_ui):
    board_ids = cmds.textScrollList(boards_ui[LIST_KEY], query=True, selectUniqueTagItem=True)
    list_ids = cmds.textScrollList(lists_ui[LIST_KEY], query=True, selectUniqueTagItem=True)
    card_ids = cmds.textScrollList(cards_ui[LIST_KEY], query=True, selectUniqueTagItem=True)

    board_id = board_ids[0] if board_ids else None
    list_id = list_ids[0] if list_ids else None
    card_id = card_ids[0] if card_ids else None

    reload_boards_select( boards_ui, lists_ui, cards_ui, card_details_ui, board_id)
    reload_lists_select( boards_ui, lists_ui, cards_ui, card_details_ui, list_id)
    reload_cards_select(boards_ui, lists_ui, cards_ui, card_details_ui, card_id)

def reload_boards_select(boards_ui, lists_ui, cards_ui, card_details_ui, board_id = None):
    load_boards(boards_ui, lists_ui, cards_ui, card_details_ui)

    if board_id:
        try:
            cmds.textScrollList(boards_ui[LIST_KEY], edit=True, selectUniqueTagItem=board_id)
        except:
            pass

def add_list(boards_ui, lists_ui, cards_ui, card_details_ui):
    board_ids = cmds.textScrollList(boards_ui[LIST_KEY], query=True, selectUniqueTagItem=True)

    if not board_ids:
        cmds.confirmDialog(
            title='No Board',
            message='Please select an existing board.',
            icon='warning')
        return

    result = cmds.promptDialog(
        title='Create new list.',
        message='List name:',
        dismissString = '',
        button='Create')

    if result == 'Create':
        new_list_name = cmds.promptDialog(query=True, text=True).strip()

        if new_list_name:
            lists.create(API_TOKEN, new_list_name, board_ids[0])

    reload_lists(boards_ui, lists_ui, cards_ui, card_details_ui)

def archive_list(boards_ui, lists_ui, cards_ui, card_details_ui):
    list_ids = cmds.textScrollList(lists_ui[LIST_KEY], query=True, selectUniqueTagItem=True)

    if list_ids:
        lists.archive(API_TOKEN, list_ids[0])
        cmds.textScrollList(lists_ui[LIST_KEY], edit=True, removeAll=True)
        reload_lists(boards_ui, lists_ui, cards_ui, card_details_ui)

def reload_lists(boards_ui, lists_ui, cards_ui, card_details_ui):
    list_ids = cmds.textScrollList(lists_ui[LIST_KEY], query=True, selectUniqueTagItem=True)
    card_ids = cmds.textScrollList(cards_ui[LIST_KEY], query=True, selectUniqueTagItem=True)

    list_id = list_ids[0] if list_ids else None
    card_id = card_ids[0] if card_ids else None

    reload_lists_select(boards_ui, lists_ui, cards_ui, card_details_ui, list_id)
    reload_cards_select(boards_ui, lists_ui, cards_ui, card_details_ui, card_id)

def reload_lists_select(boards_ui, lists_ui, cards_ui, card_details_ui, list_id = None):
    load_lists(boards_ui, lists_ui, cards_ui, card_details_ui)

    if list_id:
        try:
            cmds.textScrollList(lists_ui[LIST_KEY], edit=True, selectUniqueTagItem=list_id)
        except:
            pass

def add_card(boards_ui, lists_ui, cards_ui, card_details_ui):
    list_ids = cmds.textScrollList(lists_ui[LIST_KEY], query=True, selectUniqueTagItem=True)

    if not list_ids:
        cmds.confirmDialog(
            title='No List',
            message='Please select an existing list.',
            icon='warning')
        return

    result = cmds.promptDialog(
        title='Create new card.',
        message='Card name:',
        dismissString = '',
        button='Create')

    if result == 'Create':
        new_card_name = cmds.promptDialog(query=True, text=True).strip()

        if new_card_name:
            cards.create(API_TOKEN, new_card_name, '', list_ids[0])

    reload_cards(boards_ui, lists_ui, cards_ui, card_details_ui)

def delete_card(boards_ui, lists_ui, cards_ui, card_details_ui):
    card_ids = cmds.textScrollList(cards_ui[LIST_KEY], query=True, selectUniqueTagItem=True)

    if card_ids:
        cards.delete(API_TOKEN, card_ids[0])
        cmds.textScrollList(cards_ui[LIST_KEY], edit=True, removeAll=True)
        reload_cards(boards_ui, lists_ui, cards_ui, card_details_ui)

def reload_cards(boards_ui, lists_ui, cards_ui, card_details_ui):
    current_card_ids = cmds.textScrollList(cards_ui[LIST_KEY], query=True, selectUniqueTagItem=True)

    card_id = current_card_ids[0] if current_card_ids else None

    reload_cards_select(boards_ui, lists_ui, cards_ui, card_details_ui, card_id)

def reload_cards_select(boards_ui, lists_ui, cards_ui, card_details_ui, card_id = None):
    load_cards(lists_ui, cards_ui, card_details_ui)

    if card_id:
        try:
            cmds.textScrollList(cards_ui[LIST_KEY], edit=True, selectUniqueTagItem=card_id)
            load_card(boards_ui, lists_ui, cards_ui, card_details_ui)
        except:
            pass

def send_to_list(boards_ui, lists_ui, cards_ui, card_details_ui, card_id, list_id):
    cards.move(API_TOKEN, card_id, list_id)
    reload_lists_select(boards_ui, lists_ui, cards_ui, card_details_ui, list_id)
    reload_cards_select(boards_ui, lists_ui, cards_ui, card_details_ui, card_id)

def save_card(boards_ui, lists_ui, cards_ui, card_details_ui, card_id, name_info, desc_info):
    name = cmds.textField(name_info, query=True, text=True)
    desc = cmds.scrollField(desc_info, query=True, text=True)

    cards.update(API_TOKEN, card_id, name, desc)
    reload_cards_select(boards_ui, lists_ui, cards_ui, card_details_ui, card_id)

def main_window():
    ui_title = 'trello2maya_main'

    if cmds.window(ui_title, exists=True):
        cmds.deleteUI(ui_title, window=True)

    window = cmds.window(
        ui_title,
        title='Trello2Maya',
        sizeable=True,
        maximizeButton=True,
        minimizeButton=True,
        resizeToFitChildren=True,
        widthHeight=(500, 100))

    root_layout = cmds.rowLayout(
        numberOfColumns=2,
        adjustableColumn=2,
        columnAttach2=('left', 'both'),
        columnOffset2=(MARGIN_SIZE, MARGIN_SIZE),
        rowAttach=[[1,'top', MARGIN_SIZE], [2,'both', MARGIN_SIZE]])

    cmds.setParent(root_layout)
    selector_layout = cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=MARGIN_SIZE)
    boards_ui = lister_ui(selector_layout, 'Boards', 4)
    lists_ui = lister_ui(selector_layout, 'Board Lists', 4)
    cards_ui = lister_ui(selector_layout, 'List Cards', 8)

    cmds.setParent(root_layout)
    detail_layout = cmds.columnLayout(adjustableColumn=True)
    card_details_ui = card_detail_ui(detail_layout)

    add_actions(boards_ui, lists_ui, cards_ui, card_details_ui)
    load_boards(boards_ui, lists_ui, cards_ui, card_details_ui)

    cmds.showWindow(window)

def lister_ui(parent, label_text, visible_rows):
    cmds.setParent(parent)
    layout = cmds.columnLayout(adjustableColumn=True)
    cmds.rowLayout(numberOfColumns=4, adjustableColumn=1)
    title_text = cmds.text(
        label=label_text,
        height=CONTROL_HEIGHT,
        font='boldLabelFont',
        align='left')
    create_icon = cmds.iconTextButton(
        image='addCreateGeneric.png',
        height=CONTROL_HEIGHT,
        width=CONTROL_HEIGHT,
        scaleIcon=True)
    delete_icon = cmds.iconTextButton(
        image='deleteGeneric.png',
        height=CONTROL_HEIGHT,
        width=CONTROL_HEIGHT,
        scaleIcon=True)
    reload_icon = cmds.iconTextButton(
        image='reload.png',
        height=CONTROL_HEIGHT,
        width=CONTROL_HEIGHT,
        scaleIcon=True)

    cmds.setParent(layout)
    item_list = cmds.textScrollList(
        allowMultiSelection=False,
        numberOfRows=visible_rows)

    cmds.setParent(parent)

    return {
        TITLE_KEY: title_text,
        LIST_KEY: item_list,
        CREATE_KEY: create_icon,
        DELETE_KEY: delete_icon,
        RELOAD_KEY: reload_icon}

def card_detail_ui(parent):
    cmds.setParent(parent)

    card_panel = cmds.columnLayout(adjustableColumn=True, rowSpacing=5)

    cmds.setParent(parent)

    return {CARD_DETAILS_KEY: card_panel}

def add_actions(boards_ui, lists_ui, cards_ui, card_details_ui):
    cmds.iconTextButton(
        boards_ui[CREATE_KEY],
        edit=True,
        command = command_wrapper(
            add_board,
            boards_ui,
            lists_ui,
            cards_ui,
            card_details_ui))

    cmds.iconTextButton(
        boards_ui[DELETE_KEY],
        edit=True,
        command = command_wrapper(
            close_board,
            boards_ui,
            lists_ui,
            cards_ui,
            card_details_ui))

    cmds.iconTextButton(
        boards_ui[RELOAD_KEY],
        edit=True,
        command = command_wrapper(
            reload_boards,
            boards_ui,
            lists_ui,
            cards_ui,
            card_details_ui))

    cmds.textScrollList(
        boards_ui[LIST_KEY],
        edit=True,
        selectCommand=command_wrapper(
            load_lists,
            boards_ui,
            lists_ui,
            cards_ui,
            card_details_ui))

    cmds.iconTextButton(
        lists_ui[CREATE_KEY],
        edit=True,
        command = command_wrapper(
            add_list,
            boards_ui,
            lists_ui,
            cards_ui,
            card_details_ui))

    cmds.iconTextButton(
        lists_ui[DELETE_KEY],
        edit=True,
        command = command_wrapper(
            archive_list,
            boards_ui,
            lists_ui,
            cards_ui,
            card_details_ui))

    cmds.iconTextButton(
        lists_ui[RELOAD_KEY],
        edit=True,
        command = command_wrapper(
            reload_lists,
            boards_ui,
            lists_ui,
            cards_ui,
            card_details_ui))

    cmds.textScrollList(
        lists_ui[LIST_KEY],
        edit=True,
        selectCommand=command_wrapper(
            load_cards,
            lists_ui,
            cards_ui,
            card_details_ui))

    cmds.iconTextButton(
        cards_ui[CREATE_KEY],
        edit=True,
        command = command_wrapper(
            add_card,
            boards_ui,
            lists_ui,
            cards_ui,
            card_details_ui))

    cmds.iconTextButton(
        cards_ui[DELETE_KEY],
        edit=True,
        command = command_wrapper(
            delete_card,
            boards_ui,
            lists_ui,
            cards_ui,
            card_details_ui))

    cmds.iconTextButton(
        cards_ui[RELOAD_KEY],
        edit=True,
        command = command_wrapper(
            reload_cards,
            boards_ui,
            lists_ui,
            cards_ui,
            card_details_ui))

    cmds.textScrollList(
        cards_ui[LIST_KEY],
        edit=True,
        selectCommand=command_wrapper(
            load_card,
            boards_ui,
            lists_ui,
            cards_ui,
            card_details_ui))
