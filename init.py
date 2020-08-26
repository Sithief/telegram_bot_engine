from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import configparser
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import traceback
import tg_api
import bot_routes


base_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(base_path, 'log')
conf_path = os.path.join(base_path, 'bot_config.ini')
CONF = dict()


def init_logging():
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    handler = RotatingFileHandler(os.path.join(log_path, 'bot_log.log'),
                                  maxBytes=100000,
                                  backupCount=10,
                                  encoding='utf-8')
    console_handler = logging.StreamHandler()
    logging.basicConfig(
        handlers=[handler, console_handler],
        format='%(filename)-25s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
        level=logging.DEBUG,
        datefmt='%m-%d %H:%M',
    )


def logging_excepthook(exctype, value, tb):
    import logging
    import time
    init_logging()
    logging.critical(f'EXCEPTION: Type: {exctype}, Value: {value}')
    with open(os.path.join(log_path, 'bot_errors.log'), 'w') as error_file:
        error_file.write(time.asctime() + '\n')
        traceback.print_exception(exctype, value, tb, file=error_file)


def read_config():
    global CONF
    is_prod = os.environ.get('ENVIRON', None)
    if is_prod:
        CONF = {'token': os.environ.get('TOKEN'),
                'DB_url': os.environ.get('DATABASE_URL'),
                'server_url': os.environ.get('SERVER_URL')}
    else:
        conf = configparser.ConfigParser()
        if conf.read(conf_path, encoding='utf-8'):
            CONF = {'token': conf.get('TG', 'token'),
                    'DB_url': conf.get('DB', 'url'),
                    'server_url': conf.get('SERVER', 'url')}

        else:
            conf['TG'] = {'token': ''}
            conf['DB'] = {'url': ''}
            conf['SERVER'] = {'url': ''}
            with open(conf_path, 'w', encoding='utf-8') as configfile:
                conf.write(configfile)
            exit(0)


read_config()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONF['DB_url']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

bot_api = tg_api.TgApi(CONF.get('token'))
bot_app = bot_routes.Bot()

init_logging()
sys.excepthook = logging_excepthook
