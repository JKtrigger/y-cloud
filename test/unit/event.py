import copy
import json

_from_user = {
    'update_id': 518972469,
    'message': {
        'message_id': 23,
        'from': {
            'id': 1,
            'is_bot': False,
            'first_name': 'Any',
            'last_name': 'Name',
            'username': 'optional',
            'language_code': 'ru'
        },
        'chat': {
            'id': 2,
            'first_name': 'Any',
            'last_name': 'Name',
            'username': 'optional',
            'type': 'private'
        },
        'date': 1651151842,
        'text': 'any text'
    }
}

_from_menu = {'update_id': 518972597, 'callback_query': {'id': '1260509416069384697',
                                                         'from': {'id': 293485218, 'is_bot': False,
                                                                  'first_name': 'Максим', 'last_name': 'Налимов',
                                                                  'username': 'JKtrigger', 'language_code': 'ru'},
                                                         'message': {'message_id': 192,
                                                                     'from': {'id': 5342293603, 'is_bot': True,
                                                                              'first_name': 'booking->me',
                                                                              'username': 'HelloPreBookBot'},
                                                                     'chat': {'id': 293485218, 'first_name': 'Максим',
                                                                              'last_name': 'Налимов',
                                                                              'username': 'JKtrigger',
                                                                              'type': 'private'}, 'date': 1652970722,
                                                                     'text': 'any text', 'reply_markup': {
                                                                 'inline_keyboard': [
                                                                     [{'text': '/start', 'callback_data': '1'},
                                                                      {'text': '/start', 'callback_data': '1'}],
                                                                     [{'text': '/end', 'callback_data': '2'}]]}},
                                                         'chat_instance': '7324922121627842157', 'data': '1'}}

event_text = {'body': json.dumps(_from_user)}

_event_command = copy.deepcopy(_from_user)
_event_command['message']['entities'] = [{'offset': 0, 'length': 8, 'type': 'bot_command'}]
event_command = {'body': json.dumps(_event_command)}
from_menu = {'body': json.dumps(_from_menu)}
