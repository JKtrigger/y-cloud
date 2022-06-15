import logging


__all__ = ['logger']

format_string = "[%(asctime)s] [%(levelname)s] [%(funcName)s -> %(func)s] [%(filename)s:%(lineno)s] %(message)s"
logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)


class CustomFilter(logging.Filter):
    """
    Add log formatting
    [INFO] [wrapped -> handler] botchat.py:124 ...
    """
    def filter(self, record):
        record.func = getattr(record, 'func', getattr(record, 'funcName'))
        return True


logger.addFilter(CustomFilter())
handler = logging.StreamHandler()
handler.setLevel(logging.NOTSET)
formatter = logging.Formatter(format_string)
handler.setFormatter(formatter)
logger.addHandler(handler)
