import bot_core


@bot_core.bot_app.route('test')
def test(msg):
    bot_core.bot_api.msg_send(chat_id=msg['message']['from']['id'], text='Hello!')


bot_core.run()
