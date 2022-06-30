from src.telegram.v1 import Event, response, HTTP200
from src.telegram.v1.botchat import Listener


@response(HTTP200)
def main_menu(body: dict, chat_id):
    return {
            'method': 'sendMessage',
            'chat_id': chat_id,
            'text': 'any text',
            'reply_markup': {'keyboard': [
                ['🏠 Дом', '☭ Участок'],
                ['⚓ Море' 'Назад']
            ], 'resize_keyboard': True},
        }


@response(HTTP200)
def photo(body: dict, chat_id):
    return {
            'method': 'sendMessage',
            'chat_id': chat_id,
            'text': 'any text',
            'reply_markup': {'keyboard': [
                ['🏠 Дом', '☭ Участок'],
                ['⚓ Море', 'Назад']
            ], 'resize_keyboard': True},
        }


listener = Listener()
listener.add(main_menu, Event.Type.COMMAND, '/start')
listener.add(photo, Event.Type.TEXT, 'Посмотреть фото')
listener.add(main_menu, Event.Type.TEXT, 'Назад')