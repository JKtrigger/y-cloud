import json
import os
import uuid
from datetime import datetime

from src.telegram import BotChat, CommandHandler, CallbackHandler, TextHandler, PaymentHandler
from src.telegram.bot_calendar import TelegramCalendar

commands = CommandHandler()
callbacks = CallbackHandler()
texts = TextHandler()
payment = PaymentHandler()


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


def month_selector(request: BotChat):
    to_day = datetime.today()
    dict_calendar: dict = TelegramCalendar().to_telegram(to_day.year, to_day.month)
    dived_num = 4
    rest_division = len(dict_calendar) % dived_num
    is_full_row = rest_division == 0
    len_lines = len(dict_calendar) // dived_num + int(not is_full_row)
    inline_keyboard = []
    buttons = [{"text": month_name, "callback_data": month_name} for month_name in dict_calendar]
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
            'method': 'sendMessage',
            'chat_id': request.chat_id,
            'text': 'Выбери месяц',
            'reply_markup': {
                'inline_keyboard': inline_keyboard,
                'resize_keyboard': True
            },
        })
    }


def jul(request: BotChat):
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
                'inline_keyboard': [[{"text": "_", "callback_data": "1"}]],
                'resize_keyboard': True
            },
        })
    }


def payments(request: BotChat):
    payment_token = os.environ["payment_token"]
    print(f"payments:{payment_token}")
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'isBase64Encoded': False,
        'body': json.dumps({
            'message_id': request.message_id,
            'method': 'sendInvoice',
            'chat_id': request.chat_id,
            'text': 'Оплата',
            'provider_token': payment_token,
            'currency': 'rub',
            'title': '123',
            'description': '123',
            'payload': {
                'unique_id': str(uuid.uuid4()),
                'provider_token': os.environ["payment_token"]
                },
            'start_parameter': str(uuid.uuid4()),
            'protect_content': False,
            'prices': [{"label": "Мега", "amount": 10 * 100}],
            'need_phone_number': True,
            'send_phone_number_to_provider': True,
            'provider_data': json.dumps({
                'phone_number': '+79210071773',
                'receipt': {'items': [{
                    'description': 'Вжик',
                    'quantity': '1.00',
                    'amount': {'value': '10.00',  'currency': 'RUB'},
                    'vat_code': 1
                }]}
            })
        })
    }


def invoice_payload(request: BotChat):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'isBase64Encoded': False,
        'body': json.dumps({
            'message_id': request.message_id,
            'method': 'answerPreCheckoutQuery',
            'pre_checkout_query_id': 1,
            'ok': True
        })
    }


# The idea is getting fast fail cases first
commands.add_handler(start, '/start')
texts.add_handler(start, 'Назад')
texts.add_handler(payments, 'Оплатить бронь')
texts.add_handler(photo, 'Посмотреть фото')
texts.add_handler(month_selector, 'Выбрать даты')
texts.add_handler(month_selector, '/1')
commands.add_handler(photo, '/Const')
callbacks.add_handler(month_selector, '1')
callbacks.add_handler(jul, 'jul')
commands.add_handler(month_selector, '/1')
payment.add_handler(invoice_payload, 'invoice_payload')
