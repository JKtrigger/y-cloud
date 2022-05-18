import pytest

from src import telegram
from test.unit.event import event_text, event_command


@pytest.mark.parametrize(
    "data, expected",
    [
        (event_text, False),
        (event_command, True)
    ]
)
def test_botchat_message_type(data, expected):
    assert telegram.BotChat(data).command == expected
