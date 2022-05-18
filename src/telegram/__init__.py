from .botchat import *
from .command import *

HTTP200: int = 200
CONTENT_TYPE: str = 'application/json'
IS_BASE64_ENCODED: bool = False
HEADERS: dict = {'Content-Type': CONTENT_TYPE}
METHOD: str = 'sendMessage'


def minimal_response() -> dict:
    return {
        'statusCode': HTTP200,
        'headers': {'Content-Type': CONTENT_TYPE},
        'isBase64Encoded': IS_BASE64_ENCODED,
        'body': ''
    }
