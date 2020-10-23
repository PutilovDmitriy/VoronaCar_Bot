import os

import requests


def send_data(chat_id, text, name):
    requests.post(os.environ['SUPPORT_BOT_URL'],
                  data={'chatId': chat_id, 'message': text, 'name': name})
