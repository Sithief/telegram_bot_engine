import requests
import logging
import time


class TgApi:
    def __init__(self, token):
        self.url = f"https://api.telegram.org/bot{token}/"
        self.session = requests.Session()

    def request_get(self, method, parameters=None):
        try:
            if parameters:
                response = self.session.post(self.url + method, json=parameters)
            else:
                response = self.session.post(self.url + method)
            if response.ok:
                response_json = response.json()
                logging.debug(f'api: method: {method}, params: {parameters}, response: {response_json}')
                return response_json
            else:
                logging.error(f'connection status code = {response.status_code}, url: {self.url + method}')
        except requests.exceptions.RequestException as error_msg:
            logging.error(f'connection problems {error_msg}')
            time.sleep(1)
            return self.request_get(method, parameters)

        except Exception as error_msg:
            logging.error(f'{error_msg}')
            return {}

    def msg_send(self, chat_id, text, reply_markup):
        return self.request_get('sendMessage', {'chat_id': chat_id,
                                                'text': text,
                                                'reply_markup': reply_markup})

    def send_photo(self, chat_id, photo_url=None, photo_file=None, caption='', reply_markup=None):
        if photo_url:
            return self.request_get('sendPhoto', {'chat_id': chat_id,
                                                  'caption': caption,
                                                  'photo': photo_url,
                                                  'reply_markup': reply_markup})
