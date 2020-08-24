import configparser
import tg_api

config = configparser.ConfigParser()
if not config.read('bot_config.ini', encoding='utf-8'):
    print('Необходимо заполнить файл "bot_config.ini"')
    exit(1)
api = tg_api.TgApi(config.get('TG_API', 'token'))
print(api.request_get('getMe'))
