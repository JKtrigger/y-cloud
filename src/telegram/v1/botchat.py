import json
from .utils import logger

__all__ = ['Event', 'listener']


class Event:
    class Type:
        COMMAND = 'command'
        TEXT = 'text'
        CALLBACK = 'callback'
        PAYMENT = 'payment'

    __type_mapping = {
        'callback_query': Type.CALLBACK,
        'pre_checkout_query': Type.PAYMENT,
        'entities': Type.COMMAND
        # text used as default value
    }

    __event_key_word_mapping = {
        Type.TEXT: lambda body: body['message']['text'],
        Type.CALLBACK: lambda x: x,
        Type.PAYMENT: lambda x: x,
        Type.COMMAND: lambda body: body['message']['text'],
    }

    def __init__(self, event: json):
        self.body = json.loads(event['body'])
        self.type = self.define_type()
        self.key = self.define_key()

    def define_key(self):
        return self.__event_key_word_mapping[self.type](self.body)

    def define_type(self):
        for type_ in self.__type_mapping:
            if type_ in self.body.get('message'):
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
        logger.info(f'{event.body=}', extra={'func': func.__name__})
        return func(event.body)


listener = Listener()

