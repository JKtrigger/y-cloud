from .application import commands
from .telegram import BotChat


def handler(event, _context):
    return commands.execute(BotChat(event))
