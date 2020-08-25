from flask import request, url_for
import time
from init import *

uptime = time.time()


@app.route('/tg_callback/', methods=['POST'])
def tg_callback():
    content = request.get_json(force=True)
    print('content', content)
    # bot_api.msg_send(content['message']['from']['id'], 'привет')
    bot_api.send_photo(chat_id=content['message']['from']['id'],
                       photo_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwW1ni-5CMPTm8X3jeu9ccG7qRlHb_-oYECjyuRs_0CffKVGDl&s')
    return 'Ok'


@app.route("/")
def index():
    return f'server working {round(time.time() - uptime, 1)} seconds'


if __name__ == '__main__':
    bot_api.request_get('setWebhook', {'url': CONF.get('server_url') + '/tg_callback/'})
    app.run(debug=False)
