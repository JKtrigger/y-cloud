import json
import logging
from functools import wraps


__all__ = ['logger', 'response', 'HTTP200', 'HTTP500', 'HTTP400']


HTTP500 = 500
HTTP400 = 400
HTTP200 = 200


class CustomFilter(logging.Filter):
    """
    Add value func to formatter
    [2022-06-15 12:37:37,538] [INFO] [wrapped -> handler] botchat.py:124 ...
    """
    def filter(self, record):
        record.func = getattr(record, 'func', getattr(record, 'funcName'))
        return True


def define_logger():
    format_string = "[%(asctime)s] [%(levelname)s] [%(funcName)s -> %(func)s] [%(filename)s:%(lineno)s] %(message)s"
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.NOTSET)
    _logger.addFilter(CustomFilter())
    handler = logging.StreamHandler()
    handler.setLevel(logging.NOTSET)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    return _logger


logger = define_logger()


def response(status):
    def wrapped(func):
        @wraps(func)
        def inner(body, chat_id=None):
            result = {
                'statusCode': status,
                'headers': {'Content-Type': 'application/json'},
                'isBase64Encoded': False,
                'body': json.dumps(func(body, chat_id))
            }
            return result
        return inner
    return wrapped
