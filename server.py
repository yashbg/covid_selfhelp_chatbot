from bot import telegram_chatbot

bot = telegram_chatbot('config.cfg')

def answer_query(data, chat_id, callback_id):
    bot.answer_callback_query(callback_id)
    reply = 'You selected ' + data + '. '
    bot.send_message(reply, chat_id)

def make_reply(msg):
    if msg is not None:
        reply = 'Hello. I am the COVID Self Help Chatbot. \nPlease select a number: '
    return reply

update_id = None
while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates['result']
    if updates:
        for item in updates:
            update_id = item['update_id']
            if 'callback_query' in item:
                item = item['callback_query']
                callback_id = item['id']
                from_ = item['from']['id']
                data = item['data']
                answer_query(data, from_, callback_id)
            elif 'message' in item:
                item = item['message']
                from_ = item['from']['id']
                message = item['text']
                reply = make_reply(message)
                bot.send_message_inline(reply, from_)
