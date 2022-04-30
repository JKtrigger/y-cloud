from src import index
from test.unit import event


def test_check_endpoint():
    assert index.handler(event.from_user, context={}), "endpoint does\'t work"


