import json

from src.application import main_key_board, test
from src.index import entry_point
from src.telegram.utils import response_200
from test.bin import uncode_event
from test.bin.uncode_event import test_body_endpoint
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


def test_test_endpoint():
    _body, _chat_id = {}, 4
    result = response_200(test)({}, 4)
    chat_id = json.loads(json.loads(result["body"])['body'])['chat_id']
    text = json.loads(json.loads(result["body"])['body'])['text']
    assert chat_id == _chat_id
    assert text == f"{_body=}"


def test_wrapper():

    def decorator(argument):
        def wrapper(a, b):
            result = argument(a, b)
            print(f"\n{a} + ", f"{b} = ", f"{result}")
            return result
        return wrapper

    @decorator
    def func(a, b):
        return a + b

    def func2(a, b):
        return a + b

    assert func(1, 1) == 2
    assert func(10, -5) == 5

    assert decorator(func2)(10, -5) == 5
    assert decorator(func2)(1, 1) == 1

