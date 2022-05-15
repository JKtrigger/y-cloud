# import json


def handler(event, context):
    # body = json.loads(event['body'])
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        # 'body': json.dumps({
        #     'method': 'sendMessage',
        #     'chat_id': body['message']['chat']['id'],
        #     'text':  {
        #         "keyboard": [["uno :+1:"],
        #                      ["uno \ud83d\udc4d", "due"],
        #                      ["uno", "due", "tre"],
        #                      ["uno", "due", "tre", "quattro"]]
        #     },
        #     "reply_markup": {"ReplyKeyboardMarkup": {
        #         "keyboard": [
        #             [{"KeyboardButton": {"text": "test1"}}]]}},
        # }),
        "reply_markup": {
            "inline_keyboard": [[
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
        'isBase64Encoded': False
    }
