from src import telegram
from src.application import texts
from test.bin.uncode_event import request_from_button
from test.unit.event import event_command


def start(request: telegram.BotChat):
    return "123"


def test_request_handle():
    bot_chat = telegram.BotChat(event_command)
    bot_chat.text = '/start'
    requests_handler = telegram.CommandHandler()
    requests_handler.add_handler(start, '/start')
    assert requests_handler.execute(bot_chat) == "123"


# def test_request_unicode():
#     bot_chat = telegram.BotChat(request_from_button)
#     import ipdb
#     ipdb.set_trace() # FIXME
#     texts.execute(bot_chat)
#     import ipdb
#     ipdb.set_trace() # FIXME