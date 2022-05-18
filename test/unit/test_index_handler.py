import pytest

from src import index, telegram
from test.unit import event


@pytest.fixture(scope='function')
def handler(monkeypatch):
    inst = telegram.CommandHandler()
    monkeypatch.setattr(index, 'commands', inst)
    return inst


def test_check_endpoint(handler):
    handler.add_handler(lambda x: '123', 'any text')
    assert index.handler(event.event_text, _context={}), 'endpoint does\'t work'


