import json
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
    entities: list


def event_to_dict(event: dict):
    return json.loads(event['body'])['message']


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
    def __init__(self, message: dict):
        self.message: dataclass = data_parser(message)
        self.sender: dict = self.message.sender.get('username', 'UNKNOWN')
        self.command: bool = self.message.command
        self.text: str = self.message.text
        self.chat_id: str = self.message.bot["id"]

    def __repr__(self):
        return f"{self.__class__.__name__}(sender '{self.sender}', 'command': {self.command}, 'text': {self.text})"
