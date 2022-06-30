import json
from functools import wraps

from src.telegram.v1 import Event, logger, response, HTTP200
from src.v1_application import listener


@response(HTTP200)
def error_500(text, chat_id):  # TODO  utils level application
    return {
        'method': 'sendMessage',
        'chat_id': chat_id,
        'text':  f'{500} {text}'
    }


@response(HTTP200)
def error_400(text, chat_id):  # TODO  utils level application
    return {
        'method': 'sendMessage',
        'chat_id': chat_id,
        'text':  f'{400} : {text} - Не найдена.'
    }


def event_logger(func):  # TODO  utils level application
    @wraps(func)
    def wrapped(lambda_event, context=None):
        # context -> None for local debugging
        extra = {'func': func.__name__}
        event = Event(lambda_event)
        logger.info(f'{event=}')
        chat_id = event.chat_id
        try:
            result = func(event, chat_id)
            status_code = result['statusCode']
            body = json.loads(result['body'])
            logger.info(f'{status_code=}, {body=}', extra=extra)
            return result
        except KeyError as error:
            logger.error(f'{error=}', extra=extra)
            return error_400(f'{error}', chat_id)
        except Exception as error:
            logger.error(f'{error=}', extra=extra)
            return error_500(f'{error=}', chat_id)
    return wrapped


@event_logger
def entry_point(event, chat_id):
    """handler of all calls from telegram
    """
    return listener.execute(event, chat_id)
