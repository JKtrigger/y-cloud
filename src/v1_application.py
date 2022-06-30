from src.telegram.v1 import listener, Event, response, HTTP200


@response(HTTP200)
def main_menu(body: dict):
    return {
            'method': 'sendMessage',
            'chat_id': body['message']['chat']['id'],
            'text': 'any text',
            'reply_markup': {'keyboard': [
                ['🏠 Дом', '☭ Участок'],
                ['⚓ Море' 'Назад']
            ], 'resize_keyboard': True},
        }


@response(HTTP200)
def photo(body: dict):
    return {
            'method': 'sendMessage',
            'chat_id': body['message']['chat']['id'],
            'text': 'any text',
            'reply_markup': {'keyboard': [
                ['🏠 Дом', '☭ Участок'],
                ['⚓ Море' 'Назад']
            ], 'resize_keyboard': True},
        }


listener.add(photo, Event.Type.TEXT, 'Посмотреть фото')
listener.add(main_menu, Event.Type.TEXT, 'Назад')