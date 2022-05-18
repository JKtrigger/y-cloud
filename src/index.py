import json

from .application import commands
from .telegram import BotChat


def handler(event, _context):
    body = json.loads(event['body'])
    print(body)
    return commands.execute(BotChat(event))
