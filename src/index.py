import json


def handler(event, context):
    body = json.loads(event['body'])
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'method': 'sendSticker',
            'chat_id': body['message']['chat']['id'],
            'sticker':  "=)",
        }),
        'isBase64Encoded': False
    }
