import json
from telegram import __version__


def handler(event, context):
    print(__version__)
    #body = json.loads(event['body'])
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'method': 'InputMessageContent',
            'parse_mode': 'HTML',
            'message_text':  '<html><body>Hello</body><footer>world</footer></html>',
        }),
        'isBase64Encoded': False
    }
