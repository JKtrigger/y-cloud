from src import telegram
from test.unit.event import event_command
from test.bin.payment_body import body


def start(request: telegram.BotChat):
    return "123"


def test_request_handle():
    bot_chat = telegram.BotChat(event_command)
    bot_chat.text = '/start'
    requests_handler = telegram.CommandHandler()
    requests_handler.add_handler(start, '/start')
    assert requests_handler.execute(bot_chat) == "123"


def test_payment():
    # TODO TEMP
    bot_chat = telegram.BotChat(body)
    print(bot_chat)
