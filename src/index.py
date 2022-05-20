"""Entry point to run lambda
"""
import json

from .application import commands, callbacks
from .telegram import BotChat


def default():
    """Temp code
    """
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'isBase64Encoded': False,
        'body': json.dumps({
            'method': 'sendMessage',
            'chat_id': 'default',
            'text': 'any text'
        })
    }


def handler(event, _context):
    """handler of all calls from telegram
    """
    data = BotChat(event)
    print(event)
    try:
        if data.command:
            return commands.execute(BotChat(event))
        if data.callback:
            return callbacks.execute(BotChat(event))
        return default()
    except KeyError as error:
        print(error)
        return default()
