from pytest import fixture


@fixture
def listener_fixture():
    from src.v1_application import listener
    return listener
