import json

from src.telegram import BotChat, CommandHandler, CallbackHandler

commands = CommandHandler()
callbacks = CallbackHandler()


def start(request: BotChat):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'isBase64Encoded': False,
        'body': json.dumps({
            'method': 'sendMessage',
            'chat_id': request.chat_id,
            'text': (
                'Добро пожаловать в Калининград!\n'
                'Буду рад рассказать вам о своем доме!\n'
            ),
            'reply_markup': {'keyboard': [
                ['/Посмотреть фото', '/Const', '/Выбрать даты'],
                ['/Условия Аренды', '/Оплатить бронь', '/Получить локацию'],
                ['/Связаться со мной', '/Доп услуги', '/Оставить отзыв']
            ], 'resize_keyboard': True},
        })
    }


def photo(request: BotChat):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'isBase64Encoded': False,
        'body': json.dumps({
            'method': 'sendMessage',
            'chat_id': request.chat_id,
            'text': 'any text',
            'reply_markup': {'keyboard': [
                ['/Дом', '/Участок', '/Лес'],
                ['/Назад', '/Море', '/Случайность']
            ], 'resize_keyboard': True},
        })
    }


def one(request: BotChat):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'isBase64Encoded': False,
        'body': json.dumps({
            'message_id': request.message_id,
            'method': 'editMessageText',
            'chat_id': request.chat_id,
            'text': 'any text',
            'reply_markup': {
                'inline_keyboard': [
                    [{"text": "start", "callback_data": "1"}, {"text": "start", "callback_data": "1"}],
                    [{"text": "end", "callback_data": "1"}],
                ],
                'resize_keyboard': True
            },
        })
    }


commands.add_handler(start, '/start')
commands.add_handler(start, '/Назад')
commands.add_handler(photo, '/Посмотреть фото')
commands.add_handler(photo, '/Const')
# callbacks.add_handler(one, '1')
