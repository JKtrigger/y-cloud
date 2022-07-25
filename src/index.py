"""
entry point for yandex function
"""
from src.application import listener
from src.telegram.utils import event_handler


@event_handler
def entry_point(event, chat_id):
    """handler of all calls from telegram
    """
    return listener.execute(event, chat_id)
