import boto3

from src.telegram.v1 import Event, response, HTTP200
from src.telegram.v1.botchat import Listener

endpoint_url = 'https://storage.yandexcloud.net'
prefix = 'photo/'
bucket = 'booking'

session_ = boto3.session.Session()
s3 = session_.client(service_name='s3', endpoint_url=endpoint_url)

texts = [  # TODO make possibility to change description
    """
    Атмосферное место ДОМ и БАНЯ!
    Дом сдаётся минимум на двое суток!!
    Цена указана при бронировании от 7 дней.
    Предлагаем к бронированию июль и август! 
    Свободные даты уточняйте!
    """,
    """
    Деревянный,уютный,теплый дом с баней.
    В доме имеется все необходимые для хорошего отдыха,гостинная,кухня,две спальни и два санузла.
    Максимальное количество 6 человек.Дом расположен в жилом поселке,рядом 
    автобусная остановка,до моря 10 мин ходьбы.
    Территория ухоженная,на участке есть пруд с декоративными рыбками,в пруду купаться можно!"""
    ,
    """При заезде требуется залоговая сумма 10000р. На вcякий случай""",
    """Подтверждение бронирования 10% от суммы брони. Цена зу сутки 7500р """,
    """Внимание - отмена брони до 50% при условии отмены сделки"""
]


@response(HTTP200)
def main_menu(body: dict, chat_id):
    return {
            'method': 'sendMessage',
            'chat_id': chat_id,
            'text': 'any text',
            'reply_markup': {'keyboard': [
                ['🏠 Дом', '☭ Участок'],
                ['⚓ Море', 'Назад']
            ], 'resize_keyboard': True},
        }


def get_url_photos() -> list:
    expression = f"{endpoint_url}/{bucket}/{{key}}".format
    contents = s3.list_objects(Bucket=bucket, Prefix=prefix)['Contents']
    return [expression(key=key['Key']) for key in contents if key['Size']]


def get_photos_in_media_format():
    mapping_attr: callable = lambda x: {'type': 'photo', 'media': x}
    return [mapping_attr(i) for i in get_url_photos()]


@response(HTTP200)
def photo(body: dict, chat_id):
    return {
            'method': 'sendMediaGroup',  # is can be sending as document ?  sendDocument
                                         # sendPhoto sendMediaGroup,
            'allow_sending_without_reply': False,
            'chat_id': chat_id,
            'media': get_photos_in_media_format(),
            'protect_content': True,
            'reply_markup': {'keyboard': [
                ['🏠 Дом', '☭ Участок'],
                ['⚓ Море', 'Назад']
            ], 'resize_keyboard': True},
        }


listener = Listener()
listener.add(main_menu, Event.Type.COMMAND, '/start')
listener.add(photo, Event.Type.TEXT, 'Посмотреть фото')
listener.add(main_menu, Event.Type.TEXT, 'Назад')