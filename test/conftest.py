from pytest import fixture


@fixture
def listener_fixture():
    from src.application import listener
    return listener
