from src.telegram.v1 import botchat
from test.bin import uncode_event


def test_handler_v1():
    botchat.entry_point(uncode_event.request_from_button)
