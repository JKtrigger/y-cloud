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
            # 'text':  {
            #     "keyboard": [["uno :+1:"],
            #                  ["uno \ud83d\udc4d", "due"],
            #                  ["uno", "due", "tre"],
            #                  ["uno", "due", "tre", "quattro"]]
            # },
            "ReplyKeyboardMarkup": {
                "keyboard": [
                    [{"KeyboardButton": {"text": "test"}}]]},
        }),
        "ReplyKeyboardMarkup": {
            "keyboard": [
                [{"KeyboardButton": {"text": "test"}}]]},
        'isBase64Encoded': False
    }
