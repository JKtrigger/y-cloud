import json
from functools import wraps

from src.telegram.v1 import utils

HTTP500 = 500
HTTP200 = 200


class Event:
    class Type:
        COMMAND = 'command'
        TEXT = 'text'
        CALLBACK = 'callback'
        PAYMENT = 'payment'

    __type_mapping = {
        'callback_query': Type.CALLBACK,
        'pre_checkout_query': Type.PAYMENT,
        'command': Type.COMMAND
        # text used as default value
    }

    __event_key_word_mapping = {
        Type.TEXT: lambda body: body['message']['text'],
        Type.CALLBACK: lambda x: x,
        Type.PAYMENT: lambda x: x,
        Type.COMMAND: lambda x: x,
    }

    def __init__(self, event: json):
        self.body = json.loads(event['body'])
        self.type = self.define_type()
        self.key = self.define_key()

    def define_key(self):
        return self.__event_key_word_mapping[self.type](self.body)

    def define_type(self):
        for type_ in self.__type_mapping:
            if type_ in self.body:
                return self.__type_mapping[type_]
        return self.Type.TEXT

    def __repr__(self):
        return f"{self.__class__.__name__}({self.type=}, {self.body=})"

    def __str__(self):
        return repr(self)


class Listener:
    def __init__(self):
        self.functions = {
            Event.Type.TEXT: {},
            Event.Type.COMMAND: {},
            Event.Type.PAYMENT: {},
            Event.Type.CALLBACK: {},
        }

    def add(self, function: callable, event_type: str, key_word: str):
        events = self.functions[event_type]
        events.update({key_word: function})

    def _actions_by_type(self, event_type):
        return self.functions[event_type]

    def execute(self, event: Event):
        func = self._actions_by_type(event.type)[event.key]
        utils.logger.info(f'{event.body=}', extra={'func': func.__name__})
        return func(event.body)


listener = Listener()


def response(status):
    def wrapped(func):
        @wraps(func)
        def inner(body):
            result = {
                'statusCode': status,
                'headers': {'Content-Type': 'application/json'},
                'isBase64Encoded': False,
                'body': json.dumps(func(body))
            }
            return result
        return inner
    return wrapped


@response(HTTP200)
def photo(body: dict):
    return {
            'method': 'sendMessage',
            'chat_id': body['message']['chat']['id'],
            'text': 'any text',
            'reply_markup': {'keyboard': [
                ['Дом', 'Участок', 'Лес'],
                ['Назад', 'Море', 'Случайность']
            ], 'resize_keyboard': True},
        }


listener.add(photo, Event.Type.TEXT, 'Посмотреть фото')
listener.add(photo, Event.Type.TEXT, 'Назад')


@response(HTTP500)
def error_response(text):
    return {
        'method': 'sendMessage',
        'chat_id': 'default',
        'text':  f'Ошибка при выполнении операции :  {text}',
    }


def event_logger(func):
    @wraps(func)
    def wrapped(lambda_event, context=None):
        # context -> None for local debugging
        extra = {'func': func.__name__}
        try:
            result = func(Event(lambda_event))
            status_code = result['statusCode']
            body = json.loads(result['body'])
            utils.logger.info(f'{status_code=}, {body=}', extra=extra)
            return result
        except Exception as err:
            # TODO add test for this
            utils.logger.error_response(f'{err=}', extra=extra)
            return error_response(f'{type(err)} > {err=}')
    return wrapped


@event_logger
def entry_point(event):
    """handler of all calls from telegram
    """
    return listener.execute(event)
