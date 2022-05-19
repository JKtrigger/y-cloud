import json

from src.telegram import BotChat, CommandHandler

commands = CommandHandler()


def start(request: BotChat):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'isBase64Encoded': False,
        'body': json.dumps({
            'method': 'sendMessage',
            'chat_id': request.chat_id,
            'text': 'any text',
            'reply_markup': {'keyboard': [
                ['/start', '/start'],
                ['/end', '/end']
            ], 'resize_keyboard': True},
        })
    }


def end(request: BotChat):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'isBase64Encoded': False,
        'body': json.dumps({
            'method': 'sendMessage',
            'chat_id': request.chat_id,
            'text': 'any text',
            'reply_markup': {'inline_keyboard': [
                [{"text": "/start", "callback_data": "1"}, {"text": "/start", "callback_data": "1"}],
                [{"text": "/end", "callback_data": "2"}],
            ], 'resize_keyboard': True},
        })
    }


commands.add_handler(start, '/start')
commands.add_handler(end, '/end')
