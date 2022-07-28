import json
import logging
from calendar import HTMLCalendar, month_abbr
from collections import defaultdict
from datetime import datetime
from functools import wraps

__all__ = [
    'logger', 'Event', 'calendar', 'listener', 'response_200', 'event_handler'
    ]


class CustomFilter(logging.Filter):
    """
    Add value func to formatter
    [2022-06-15 12:37:37,538] [INFO] [wrapped -> handler]  ...
    """
    def filter(self, record):
        record.func = getattr(record, 'func', getattr(record, 'funcName'))
        return True


def define_logger():
    format_string = (
        "[%(asctime)s] [%(levelname)s] [%(funcName)s -> %(func)s]"
        " [%(filename)s:%(lineno)s] %(message)s"
    )
    _logger = logging.getLogger(__name__)
    _logger.addFilter(CustomFilter())
    _logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    return _logger


def response_200(func):
    @wraps(func)
    def inner(body, chat_id=None):
        result = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'isBase64Encoded': False,
            'body': json.dumps(func(body, chat_id))
        }
        return result
    return inner


@response_200
def error_500(text, chat_id):
    """Function to avoid repeating events in yandex functions
    """
    return {
        'method': 'sendMessage',
        'chat_id': chat_id,
        'text':  f'Error: {text}'
    }


def event_handler(func):
    @wraps(func)
    def wrapped(lambda_event, context=None):
        event = Event(lambda_event)
        try:
            logger.info(f'{event=}')
            result = func(event, event.chat_id)
            status_code = result['statusCode']
            body = json.loads(result['body'])
            logger.info(f'{status_code=}, {body=}')
            return result
        except Exception as error:
            logger.error(f'{error=}')
            return error_500(f'{error=}', event.chat_id)
    return wrapped


def default_callback():
    return response_200(_define_month_callback)


def _define_month_callback(body, chat_id):
    week_names = [
        {'text': 'ПН', 'callback_data': 'ignore'},
        {'text': 'ВТ', 'callback_data': 'ignore'},
        {'text': 'СР', 'callback_data': 'ignore'},
        {'text': 'ЧТ', 'callback_data': 'ignore'},
        {'text': 'ПТ', 'callback_data': 'ignore'},
        {'text': 'СБ', 'callback_data': 'ignore'},
        {'text': 'ВС', 'callback_data': 'ignore'},
    ]
    text = body['callback_query']['data']  # month
    if body['callback_query']['data'] in calendar.months:
        days = calendar.months[text]
        buttons = map(
            lambda week: [
                {
                    'text': day,
                    'callback_data':
                        f'{calendar.to_day.year}-{text}-{day}' if day != '_' else 'ignore'
                }
                for day in week], days
        )
        return {
            'message_id': body['callback_query']['message']['message_id'],
            'method': 'editMessageText',
            'chat_id': chat_id,
            'text': f'{text}',
            'reply_markup': {
                'inline_keyboard': [week_names, *buttons],
                'resize_keyboard': True
            },
        }

    date = datetime.strptime(body['callback_query']['data'], '%Y-%b-%d')
    return {
        'message_id': body['callback_query']['message']['message_id'],
        'method': 'editMessageText',
        'chat_id': chat_id,
        'text': f'С {date.date()}. Количество дней 1',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {'text': '-', 'callback_data': 'minus'},
                    {'text': '+', 'callback_data': 'plus'}
                ],
                [
                    {'text': 'Оплатить', 'callback_data': 'payment'}
                ]
            ],
            'resize_keyboard': True
        },
    }
    # TODO
    # check phrase in text (С 1 - по )
    # check is available date from yandex calendar
    # change text


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
        # TODO
        Type.TEXT: lambda body: body['message']['text'],
        Type.CALLBACK: lambda body: body['callback_query']['data'],
        Type.PAYMENT: lambda x: x,
        Type.COMMAND: lambda body: body['message']['text'],
    }
    __chat_id_mapping = {
        Type.TEXT: lambda body: body['message']['chat']['id'],
        Type.CALLBACK: lambda body: body['callback_query']['message']['chat']['id'],
        Type.PAYMENT: lambda x: x,
        Type.COMMAND: lambda body: body['message']['chat']['id'],
    }

    def define_chat_id(self):
        return self.__chat_id_mapping[self.type](self.body)

    def __init__(self, event: json):
        self.body = json.loads(event['body'])
        self.type = self.define_type()
        self.key = self.define_key()
        self.chat_id = self.define_chat_id()

    def define_key(self):
        return self.__event_key_word_mapping[self.type](self.body)

    def define_type(self):
        for type_ in self.__type_mapping:
            if type_ in self.body:
                return self.__type_mapping[type_]
            if 'message' in self.body:
                if type_ in self.body['message']:
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
            Event.Type.CALLBACK:  defaultdict(default_callback),
        }

    def add(self, function: callable, event_type: str, key_word: str):
        events = self.functions[event_type]
        events.update({key_word: function})

    def _actions_by_type(self, event_type):
        return self.functions[event_type]

    def execute(self, event: Event, chat_id):
        func = self._actions_by_type(event.type)[event.key]
        logger.info(f'{event.body=}', extra={'func': func.__name__})
        return func(event.body, chat_id)


class TelegramCalendar(HTMLCalendar):
    def formatday(self, day, weekday):
        """Return a day as a table cell.
        """
        if day == 0:
            return '_'
        return str(day)

    def formatweek(self, week):
        return [self.formatday(d, wd) for (d, wd) in week]

    def formatmonth(self, year, month, with_year=False):
        return [self.formatweek(week) for week in self.monthdays2calendar(year, month)]

    def format_period(self, year, month):
        month_names = [*month_abbr]
        result = {}
        days_in_month_to_end_of_year = [self.formatmonth(year, m) for m in range(month, 13)]
        for days_in_week in days_in_month_to_end_of_year:
            result[month_names[month].lower()] = days_in_week
            month += 1
        return result


class CalendarChain:
    to_day: datetime = datetime.today()
    months: dict = TelegramCalendar().format_period(to_day.year, to_day.month)
    buttons_in_line = 4
    chain_ignore = "ignore"

    @property
    def month_buttons(self):
        self._pre_define_month_buttons()
        self._define_month_buttons()
        self._post_define_month_buttons()
        return self.inline_keyboard

    def _define_month_buttons(self):
        """Populate buttons for line in menu lines
        """
        self.inline_keyboard = []
        buttons = [{"text": month_name, "callback_data": month_name} for month_name in self.months]
        bil = self.buttons_in_line
        for index in range(0, self.menu_lines):
            self.inline_keyboard.append(buttons[index * bil: index * bil + bil])

    def _pre_define_month_buttons(self):
        """Define numbers of menu lines
        """
        self.rest_division = len(self.months) % self.buttons_in_line
        self.is_full_row = self.rest_division == 0
        additional_line = int(not self.is_full_row)
        self.menu_lines = len(self.months) // self.buttons_in_line + additional_line

    def _post_define_month_buttons(self):
        """Define behavior to missing buttons and the last one button
        """
        if not self.is_full_row:
            last_menu_item = self.inline_keyboard[self.menu_lines - 1]
            for each_missing_button in range(0, self.buttons_in_line - self.rest_division):
                last_menu_item.append({"text": "_", "callback_data": self.chain_ignore})


logger = define_logger()
listener = Listener()
calendar = CalendarChain()
