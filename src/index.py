"""Entry point to run lambda
"""
import json

from .application import commands, callbacks, texts
from .telegram import BotChat


def default(text):
    """Temp code
    """
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'isBase64Encoded': False,
        'body': json.dumps({
            'method': 'sendMessage',
            'chat_id': 'default',
            'text': text
        })
    }


def handler(event, _context):
    """handler of all calls from telegram
    """
    data = BotChat(event)
    print(f"{event=}")
    print(f"{data=}")
    try:
        if data.command:
            return commands.execute(BotChat(event))
        if data.callback:
            return callbacks.execute(BotChat(event))
        if not (data.command and data.callback):
            return texts.execute(BotChat(event))
        return default(text="not found")
    except KeyError as error:
        print(error)
        return default(text=str(error))
