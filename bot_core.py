from flask import request, url_for
import time
from init import *

uptime = time.time()


@app.route('/tg_callback/', methods=['POST'])
def tg_callback():
    content = request.get_json(force=True)
    print('content', content)
    return 'Ok'


@app.route("/")
def index():
    return f'server working {round(time.time() - uptime, 1)} seconds'


if __name__ == '__main__':
    bot_api.request_get('setWebhook', {'url': CONF.get('server_url') + '/tg_callback/'})
    app.run(debug=False)
