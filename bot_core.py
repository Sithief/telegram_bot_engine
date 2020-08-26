from flask import request
import time
from init import *

uptime = time.time()


def message_processing(content):
    if 'message' in content:
        menu_function = bot_app.serve('text')
    elif 'callback_query' in content:
        menu_function = bot_app.serve('callback')
    else:
        menu_function = bot_app.serve('other')
    menu_function(content)


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
