import json
import time
from copy import copy
from dataclasses import dataclass

from dacite import from_dict

__all__ = ["BotChat"]


@dataclass
class Message:
    message_id: int
    sender: dict
    bot: dict
    date: int
    text: str
    command: bool
    request: str
    callback: bool  # TODO REFACTOR NAMES AND TYPES
    entities: list
    payment: bool


def event_to_dict(event: dict):
    body = json.loads(event['body'])
    if 'callback_query' in body:
        message = body['callback_query']['message']
        message['callback'] = True
        message['request'] = body['callback_query']['data']
        message['payment'] = False
    elif 'pre_checkout_query' in body:
        # TODO to many responsibility
        message = body['pre_checkout_query']
        message['callback'] = False
        message['request'] = ''
        message['payment'] = True
        message['chat'] = copy(message['from'])
        message['message_id'] = int(message['id'])
        message['date'] = int(time.time())
        message['text'] = 'invoice_payload'
    else:
        message = body['message']
        message['callback'] = False
        message['request'] = ''
        message['payment'] = False
    return message


def attrs_rename(message: dict):
    message['sender'] = message.pop('from')
    message['bot'] = message.pop('chat')


def pre_populate_attrs(message: dict):
    message['entities'] = message.get('entities', [{'type': 'message'}])
    message['command'] = message['entities'][0]['type'] == 'bot_command'


def data_parser(message):
    message: dict = event_to_dict(message)
    attrs_rename(message)
    pre_populate_attrs(message)
    return from_dict(data_class=Message, data=message)


class BotChat:
    # TODO TO MANY RESPONSIBILITY
    def __init__(self, message: dict):
        self.message: dataclass = data_parser(message)
        self.sender: dict = self.message.sender.get('username', 'UNKNOWN')
        self.command: bool = self.message.command
        self.text: str = self.message.text
        self.chat_id: str = self.message.bot["id"]
        self.request = self.message.request
        self.callback = self.message.callback
        self.message_id = self.message.message_id
        self.payment = self.message.payment

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"("
            f"sender: '{self.sender}', "
            f"command: {self.command}, "
            f"text: {self.text},"
            f"callback: {self.callback},"
            f"payment: {self.payment})"
        )


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

    def __init__(self, event: json):
        self.body = json.loads(event)['body']
        self.sender = self.body['username']
        self.type = self.define_type()

    def define_type(self):
        for type_ in self.__type_mapping:
            if type_ in self.body:
                return self.__type_mapping[type_]
        return self.Type.TEXT

    def __repr__(self):
        return f"{self.__class__.__name__}({self.type=}, {self.sender=}, {self.body=})"

    def __str__(self):
        return repr(self)


def response(status):
    def wrapped(func):
        def inner(body):
            return {
                'statusCode': status,
                'headers': {'Content-Type': 'application/json'},
                'isBase64Encoded': False,
                'body': json.dumps(func(body))
            }
        return inner
    return wrapped


HTTP500 = 500


@response(HTTP500)
def default(text):
    return {
        'method': 'sendMessage',
        'chat_id': 'default',
        'text': text
    }


def event_logger(func):
    def wrapped(lambda_event, context):
        print(f'{lambda_event=}')  # todo format to logger
        print(f'{context=}')
        try:
            result = func(Event(lambda_event))
            return result
        except Exception as err:
            print(f'{err=}')
            return default(f"{type(err)} > {err=}")
    return wrapped


@event_logger
def handler(event):
    """handler of all calls from telegram
    """
    print(f'{event=}')

