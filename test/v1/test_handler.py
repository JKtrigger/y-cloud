import json

from src.telegram.v1 import HTTP400, HTTP200
from src.v1_index import entry_point
from test.bin import uncode_event


def test_handler_un_exist_function(caplog):
    result = entry_point(uncode_event.request_photo)
    assert result['statusCode'] == HTTP400
    assert json.loads(result['body'])['text'] == "Опция : 'Посмотреть фото' - Не найдена."
    assert caplog.messages[1] == "error=KeyError('Посмотреть фото')"


def test_handler_photo(listener_fixture):
    result = entry_point(uncode_event.request_photo)
    assert result['statusCode'] == HTTP200
