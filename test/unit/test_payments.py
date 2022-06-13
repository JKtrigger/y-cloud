from src import telegram
from test.bin.payment_body import body


def test_payment():
    bot_chat = telegram.BotChat(body)
    assert bot_chat.payment
    assert bot_chat.text == 'invoice_payload'
