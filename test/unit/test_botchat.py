import pytest

from src import telegram
from test.unit.event import event_text, event_command, from_menu


@pytest.mark.parametrize(
    "data, command, callback",
    [
        (event_text, False, False),
        (event_command, True, False),
        (from_menu, False, True)
    ]
)
def test_botchat_message_type(data, command, callback):
    assert telegram.BotChat(data).command == command
    assert telegram.BotChat(data).callback == callback
