import json

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
        return self._actions_by_type(event.type)[event.key](event.body)


listener = Listener()


def response(status):
    def wrapped(func):
        # add wrap from func tools
        def inner(body):
            return {
                'statusCode': status,
                'headers': {'Content-Type': 'application/json'},
                'isBase64Encoded': False,
                'body': json.dumps(func(body))
            }
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
def error(text):
    return {
        'method': 'sendMessage',
        'chat_id': 'default',
        'text':  f'Ошибка при выполнении операции :  {text}',
    }


def event_logger(func):
    def wrapped(lambda_event, context=None):
        # context -> None for local debugging
        print(f'{lambda_event=}')  # todo format to logger debug
        print(f'{context=}')
        try:
            result = func(Event(lambda_event))
            print(f'{result=}')
            return result
        except Exception as err:
            print(f'{err=}')  # todo format to logger error
            return error(f"{type(err)} > {err=}")
    return wrapped


@event_logger
def handler(event):
    """handler of all calls from telegram
    """
    print(f'{event=}')
    return listener.execute(event)
