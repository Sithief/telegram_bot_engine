from flask import request
import time
from init import *

uptime = time.time()


def message_processing(msg):
    menu_function = bot_app.serve('test')
    menu_function(msg)


@app.route('/tg_callback/', methods=['POST'])
def tg_callback():
    content = request.get_json(force=True)
    print('content', content)
    message_processing(content)
    return 'Ok'


@app.route("/")
def index():
    return f'server working {round(time.time() - uptime, 1)} seconds'


def run():
    bot_api.request_get('setWebhook', {'url': CONF.get('server_url') + '/tg_callback/'})
    app.run()
