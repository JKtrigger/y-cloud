import json
from datetime import datetime

from src.telegram import BotChat, CommandHandler, CallbackHandler, TextHandler
from src.telegram.bot_calendar import TelegramCalendar

commands = CommandHandler()
callbacks = CallbackHandler()
texts = TextHandler()


def start(request: BotChat):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'isBase64Encoded': False,
        'body': json.dumps({
            'method': 'sendMessage',
            'chat_id': request.chat_id,
            'text': (
                'Добро пожаловать в Калининград!\n'
                'Буду рад рассказать вам о своем доме!\n'
            ),
            'reply_markup': {'keyboard': [
                ['Посмотреть фото', 'Цена', 'Выбрать даты'],
                ['Условия Аренды', 'Оплатить бронь', 'Получить локацию'],
                ['Связаться со мной', 'Доп услуги', 'Оставить отзыв']
            ], 'resize_keyboard': True},
        })
    }


def photo(request: BotChat):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'isBase64Encoded': False,
        'body': json.dumps({
            'method': 'sendMessage',
            'chat_id': request.chat_id,
            'text': 'any text',
            'reply_markup': {'keyboard': [
                ['Дом', 'Участок', 'Лес'],
                ['Назад', 'Море', 'Случайность']
            ], 'resize_keyboard': True},
        })
    }


def one(request: BotChat):
    to_day = datetime.today()
    dict_calendar: dict = TelegramCalendar().to_telegram(to_day.year, to_day.month)
    dived_num = 4
    rest_division = len(dict_calendar) % dived_num
    is_full_row = rest_division == 0
    len_lines = len(dict_calendar) // dived_num + int(not is_full_row)
    inline_keyboard = []
    buttons = [{"text": month_name, "callback_data": "1"} for month_name in dict_calendar]
    for index in range(0, len_lines):

        inline_keyboard.append(buttons[index*dived_num: index*dived_num + dived_num])
    if not is_full_row:
        for each_missing_button in range(0, 4 - rest_division):
            inline_keyboard[len_lines-1].append({"text": "_", "callback_data": "1"})

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'isBase64Encoded': False,
        'body': json.dumps({
            'message_id': request.message_id,
            'method': 'editMessageText',
            'chat_id': request.chat_id,
            'text': 'Выбери месяц',
            'reply_markup': {
                'inline_keyboard': inline_keyboard,
                'resize_keyboard': True
            },
        })
    }


commands.add_handler(start, '/start')
texts.add_handler(start, 'Назад')
texts.add_handler(photo, 'Посмотреть фото')
texts.add_handler(one, 'Выбрать даты')
commands.add_handler(photo, '/Const')
callbacks.add_handler(one, '1')
