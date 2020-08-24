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
                logging.error(f'connection status code = {response.status_code}')
        except requests.exceptions.RequestException as error_msg:
            logging.error(f'connection problems {error_msg}')
            time.sleep(1)
            return self.request_get(method, parameters)

        except Exception as error_msg:
            logging.error(f'{error_msg}')
            return {}
