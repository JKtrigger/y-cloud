# #
# import base64
#
# import requests
#
#
# def test_123():
#     url = 'https://yandex.com/dev/id/doc/dg/oauth/reference/auto-code-client.html#auto-code-client__get-token'
#     client_id = '94b04019483544628bcf5923ffa2aff4'
#     client_secret = '2fe32d3fa10b4a89ba5fff1dee652844'
#     method = 'POST'
#     # from yandex.cloud.
#     response = requests.request(
#         'get',
#         'https://calendar.yandex.com/export/ics.xml?private_token=8a993f184514cffb82b84e28a6a27f492a7d4ec9&tz_id=Asia/Tashkent',
#         headers={
#             "Content-type": 'application/x-www-form-urlencoded',
#             "Authorization": base64.b64encode(b'94b04019483544628bcf5923ffa2aff4:2fe32d3fa10b4a89ba5fff1dee652844')
#         }
#     )
#     # https://oauth.yandex.com/authorize?response_type=token&client_id=94b04019483544628bcf5923ffa2aff4&redirect_uri=yandexta://booking.website.yandexcloud.net
#     with open('booking.ics', 'w') as r:
#         r.write(response.text)
#     import ipdb
#     ipdb.set_trace() # FIXME
#
#     # Content-type: application/x-www-form-urlencoded
#     # Content-Length: <длина тела запроса>
#     # Authorization: Basic <закодированная строка client_id:client_secret>
#     pass