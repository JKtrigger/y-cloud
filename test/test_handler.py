import json

from src.application import main_key_board
from src.index import entry_point
from test.bin import uncode_event
from test.unit.event import event_command


def test_handler_un_exist_function(caplog):
    result = entry_point(uncode_event.request_unexpected)
    assert result['statusCode'] == 200, "To avoid repeating"
    assert json.loads(result['body'])['text'] == "Error: error=KeyError('request_unexpected')"
    assert caplog.messages[1] == "error=KeyError('request_unexpected')"


def test_handler_photo(listener_fixture):
    result = entry_point(uncode_event.request_photo)
    assert result['statusCode'] == 200
    assert json.loads(result['body'])["chat_id"] == 293485218


def test_start_command(listener_fixture):
    result = entry_point(event_command)
    assert result['statusCode'] == 200
    assert json.loads(result['body'])["chat_id"] == 2
    assert json.loads(result['body'])['reply_markup'] == main_key_board
