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
                ['/start', '/end'],
                ['/start', '/end']
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
            'reply_markup': {'keyboard': [
                [{"text": "FIRST_BUTTON", "otherkeys": "1"}],
                [{"text": "SECOND_BUTTON", "otherkeys": "2"}],
            ], 'resize_keyboard': True},
        })
    }


commands.add_handler(start, '/start')
commands.add_handler(end, '/end')
