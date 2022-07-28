import operator

from src.telegram.utils import Event, calendar, listener, response_200
from src.utils import get_photos_in_media_format

main_key_board = {
    'keyboard': [
            ['🏠 Дом', '☭ Участок', '📅'],
            ['⚓ Море', '📍 Локация']
    ],
    'resize_keyboard': True
}


@response_200
def main_menu(_body: dict, chat_id):
    return {
        'method': 'sendMessage',
        'chat_id': chat_id,
        'text': 'any text',
        'reply_markup': main_key_board
    }


@response_200
def photo(_body: dict, chat_id):
    return {
        'method': 'sendMediaGroup',
        'allow_sending_without_reply': False,
        'chat_id': chat_id,
        'media': get_photos_in_media_format(),
        'protect_content': True,
        'reply_markup': main_key_board
    }


@response_200
def location(_body: dict, chat_id):
    return {
        'method': 'sendLocation',
        'latitude': 54.9564385,
        'longitude': 20.260593,
        'chat_id': chat_id,
        'reply_markup': main_key_board
    }


def define_callbacks():
    for month, days in calendar.months.items():
        buttons = map(
            # TODO too hard to read
            # '%Y-%b-%d' - mask
            lambda week: [
                {
                    'text': day,
                    'callback_data':
                        f'{calendar.to_day.year}-{month}-{day}' if day != '_' else 'ignore'
                }
                # TODO 'ignore' as constant
                for day in week], days
        )

        def fun(body: dict, chat_id):
            return {
                'message_id': body['callback_query']['message']['message_id'],
                'method': 'editMessageText',
                'chat_id': chat_id,
                'text': 'Выбери день',
                'reply_markup': {
                        'inline_keyboard': [*buttons],
                        'resize_keyboard': True
                   },
            }

        listener.add(response_200(fun), Event.Type.CALLBACK, month)


@response_200
def months(_body: dict, chat_id):
    return {
        'method': 'sendMessage',
        'chat_id': chat_id,
        'text': 'Выбери месяц',
        'reply_markup': {
            'inline_keyboard': calendar.month_buttons,
            'resize_keyboard': True
        },
    }


@response_200
def ignore(_body: dict, chat_id):
    return {
        'method': 'editMessageText',
        'chat_id': chat_id,
        'text': _body['callback_query']['message']['text'],
        'reply_markup': {
            'inline_keyboard': _body['callback_query']['message']['reply_markup']['inline_keyboard'],
            'resize_keyboard': True
        }
    }


@response_200
def count_days(_body: dict, chat_id):
    operator_ = operator.sub
    if _body['callback_query']['data'] == 'plus':
        operator_ = operator.add
    text = _body['callback_query']['message']['text']
    count = [int(s) for s in text.split() if s.isdigit()][0]
    count = operator_(count, 1)
    if count == 31:
        count = 1
    if count == 0:
        count = 30
    return {
        'method': 'sendMessage',
        'chat_id': chat_id,
        'text': f"Количество дней {count}",
        'reply_markup': {
            'inline_keyboard': _body['callback_query']['message']['reply_markup']['inline_keyboard'],
            'resize_keyboard': True
        }
    }


listener.add(main_menu, Event.Type.COMMAND, '/start')
listener.add(ignore, Event.Type.CALLBACK, 'ignore')
listener.add(count_days, Event.Type.CALLBACK, 'plus')
listener.add(count_days, Event.Type.CALLBACK, 'minus')
listener.add(photo, Event.Type.TEXT, '🏠 Дом')
listener.add(location, Event.Type.TEXT, '📍 Локация')
listener.add(months, Event.Type.TEXT, '📅')
