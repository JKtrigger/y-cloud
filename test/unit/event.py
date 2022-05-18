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

event_text = {'body': json.dumps(_from_user)}

_event_command = copy.deepcopy(_from_user)
_event_command['message']['entities'] = [{'offset': 0, 'length': 8, 'type': 'bot_command'}]
event_command = {'body': json.dumps(_event_command)}
