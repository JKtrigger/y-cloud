"""Entry point to run lambda
"""
import json

from .application import commands
from .telegram import BotChat


def handler(event, _context):
    """handler of all calls from telegram
    """
    print(json.loads(event['body']))
    return commands.execute(BotChat(event))
