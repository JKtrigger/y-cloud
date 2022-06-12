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
        message['message_id'] = -1  # Negative
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
