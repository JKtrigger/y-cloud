import json
from functools import wraps

from src.telegram.v1 import listener, Event, logger, response, HTTP400, HTTP500


@response(HTTP500)
def error_500(text):  # TODO  utils level application
    return {
        'method': 'sendMessage',
        'chat_id': 'default',
        'text':  f'{text}'
    }


@response(HTTP400)
def error_400(text):  # TODO  utils level application
    return {
        'method': 'sendMessage',
        'chat_id': 'default',
        'text':  f'Опция : {text} - Не найдена.'
    }


def event_logger(func):  # TODO  utils level application
    @wraps(func)
    def wrapped(lambda_event, context=None):
        # context -> None for local debugging
        extra = {'func': func.__name__}
        try:
            logger.info(f'{Event(lambda_event)=}')
            result = func(Event(lambda_event))
            status_code = result['statusCode']
            body = json.loads(result['body'])
            logger.info(f'{status_code=}, {body=}', extra=extra)
            return result
        except KeyError as error:
            logger.error(f'{error=}', extra=extra)
            return error_400(f'{error}')
        except Exception as error:
            logger.error(f'{error=}', extra=extra)
            return error_500(f'{error=}')
    return wrapped


@event_logger
def entry_point(event):
    """handler of all calls from telegram
    """
    return listener.execute(event)
