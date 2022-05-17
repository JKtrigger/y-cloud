import json


def handler(event, context):
    body = json.loads(event['body'])
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'method': 'sendMessage',
            'chat_id': body['message']['chat']['id'],
            'text': body,
            "reply_markup": {"keyboard": [
                ["opt 1", "opt 2", "opt 3"],
                ["menu"]], "resize_keyboard": True},
        }),
        'isBase64Encoded': False
    }
