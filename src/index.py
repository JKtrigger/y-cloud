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
            "reply_markup": {
                "reply_keyboard": [[
                    {
                        "text": "A",
                        "callback_data": "A1"
                    },
                    {
                        "text": "B",
                        "callback_data": "C1"
                    }]
                ]
            },
        }),
        'isBase64Encoded': False
    }
