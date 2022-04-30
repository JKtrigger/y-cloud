import json

_from_user = {
    "update_id": 518972469,
    "message": {
        "message_id": 23,
        "from": {
            "id": 1,
            "is_bot": False,
            "first_name": "Any",
            "last_name": "Name",
            "username": "optional",
            "language_code": "ru"
        },
        "chat": {
            "id": 2,
            "first_name": "Any",
            "last_name": "Name",
            "username": "optional",
            "type": "private"
        },
        "date": 1651151842,
        "text": "any text"
    }
}
from_user = {"body": json.dumps(_from_user)}
