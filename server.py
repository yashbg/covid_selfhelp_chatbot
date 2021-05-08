from bot import telegram_chatbot
import pandas as pd

bot = telegram_chatbot('config.cfg')

def getInfo(reqmnt, state, city):
    df = pd.DataFrame([
        [reqmnt, state, city],
        [reqmnt, state, city],
    ])
    return df

def intro():
    reply = 'Hello. I am the COVID Self Help Chatbot.'
    return reply

def make_reply(msg):
    if msg is not None:
        reply = 'Please select a requirement:'
    return reply

def answer_query(response_type, reqmnt, state, city, state_list, city_list, chat_id, message_id, callback_id):
    bot.answer_callback_query(callback_id)
    if response_type == 'reqmnt':
        reply = f"Please select the state in which you want {reqmnt}:"
        bot.edit_message(reply, 'state', state_list, chat_id, message_id)
    elif response_type == 'state':
        reply = f"Please select the city in {state} where you want {reqmnt}:"
        bot.edit_message(reply, 'city', city_list, chat_id, message_id)
    elif response_type == 'city':
        info = getInfo(reqmnt, state, city)
        reply = f"Requirement: {info[0][0]}\nState: {info[1][0]}\nCity: {info[2][0]}"
        bot.send_message(reply, chat_id)

reqmnt_list = ['Plasma', 'Oxygen']
state_list = ['Assam', 'Delhi NCR']
city_list = ['Guwahati', 'Gurugram']
reqmnt = None
state = None
city = None
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
                message_id = item['message']['message_id']
                data = item['data'].split(':')
                if data[0] == 'reqmnt':
                    reqmnt = data[1]
                elif data[0] == 'state':
                    state = data[1]
                elif data[0] == 'city':
                    city = data[1]
                answer_query(data[0], reqmnt, state, city, state_list, city_list, from_, message_id, callback_id)
            elif 'message' in item:
                item = item['message']
                from_ = item['from']['id']
                message = item['text']
                reply = intro()
                bot.send_message(reply, from_)
                reply = make_reply(message)
                bot.send_message_inline(reply, 'reqmnt', reqmnt_list, from_)
