import json


def handler(event, context):
    #body = json.loads(event['body'])
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'method': 'InputMessageContent',
            'parse_mode': 'HTML',
            'text':  '<html><body>Hello</body><footer>world</footer></html>',
        }),
        'isBase64Encoded': False
    }
