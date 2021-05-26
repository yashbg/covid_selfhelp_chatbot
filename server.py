from bot import telegram_chatbot
from extract_data import *

bot = telegram_chatbot('config.cfg')

def make_intro():
    reply = 'Hello. I am the COVID Self Help Chatbot.'
    return reply

def checkna(str):
    if pd.isna(str):
        return 'Not available'
    return str

def make_reply(data=None, info=None, counter=None):
    if not isinstance(info, pd.DataFrame):
        reply = 'Please select a requirement:'
    else:
        if data[1] == 'Oxygen' or data[1] == 'Hospital Beds':
            reply = f"{data[1]} in {data[3]}:\nName: {checkna(info['name'][counter])}\nContact No.: {checkna(info['contact'][counter])}"
        elif data[1] == 'Medicines':
            reply = f"{data[1]} in {data[2]}:\nName: {checkna(info['name'][counter])}\nContact No.: {checkna(info['contact'][counter])}"
        elif data[1] == 'Plasma' and data[2] == 'Organisations':
            reply = f"{data[1]} {data[2]} in {data[3]}:\nName: {checkna(info['name'][counter])}\nContact No.: {checkna(info['contact'][counter])}"
        elif data[0] == 'plasma_donor_bloodgrp' or (data[0] == 'end' and data[1] == 'Plasma' and data[2] == 'Donors'):
            reply = f"{data[4]} {data[1]} in {data[3]}:\nName: {checkna(info['name'][counter])}\nContact No.: {checkna(info['contact'][counter])}"
        if pd.notna(info['status'][counter]):
            reply += f"\nStatus: {info['status'][counter]}"
            if info['date_time'][counter]:
                reply +=f"\nDate/Time of Verification: {info['date_time'][counter]}"
        if pd.notna(info['info'][counter]):
            reply += f"\nAdditional Info: {info['info'][counter]}"
    return reply

def make_err():
    reply = 'Sorry, there is no more data available.'
    return reply

def answer_query(data, reqmnt_list, state_list, city_list, plasma_type_list, plasma_donor_bloodgrp_list, chat_id, message_id, callback_id):
    bot.answer_callback_query(callback_id)
    if data[0] == 'start':
        reply = 'Please select a requirement:'
        bot.edit_message(reply, 'reqmnt', reqmnt_list, chat_id, message_id)
    elif data[0] == 'reqmnt':
        if data[1] == 'Plasma':
            reply = 'Please select whether you want to search for Organisations or Donors:'
            bot.edit_message(reply, 'plasma_type', plasma_type_list, chat_id, message_id, data[1])
        else:
            reply = f"Please select the state in which you want {data[1]}:"
            bot.edit_message(reply, 'state', state_list, chat_id, message_id, data[1])
    elif data[0] == 'state' and data[1] != 'Medicines':
        reply = f"Please select the city in {data[2]} where you want {data[1]}:"
        bot.edit_message(reply, 'city', city_list, chat_id, message_id, data[1], data[2])
    elif data[0] == 'plasma_type':
        reply = f"Please select the city where you want {data[1]} {data[2]}:"
        bot.edit_message(reply, 'city', city_list, chat_id, message_id, data[1], plasma_type=data[2])
    elif data[0] == 'city' and data[1] == 'Plasma' and data[2] == 'Donors':
        reply = f"Please select the blood group you want in {data[3]}:"
        bot.edit_message(reply, 'plasma_donor_bloodgrp', plasma_donor_bloodgrp_list, chat_id, message_id, data[1], plasma_type=data[2], city=data[3])
    elif data[0] == 'city' or ((data[0] == 'state' or data[0] == 'end') and data[1] == 'Medicines') or data[0] == 'plasma_donor_bloodgrp' or data[0] == 'end':
        if (data[0] == 'state' or data[0] == 'end') and data[1] == 'Medicines':
            info = get_medicine_info(data[2])
        elif data[1] == 'Plasma' and data[2] == 'Organisations':
            info = get_plasma_org_info(data[3])
        elif data[0] == 'plasma_donor_bloodgrp' or (data[0] == 'end' and data[1] == 'Plasma' and data[2] == 'Donors'):
            info = get_plasma_donor_info(data[3], data[4])
        else:
            info = get_info(data[1], data[2], data[3])
        counter = 0
        if data[0] == 'end':
            if data[1] == 'Medicines':
                counter = int(data[3])
            elif data[1] == 'Plasma' and data[2] == 'Donors':
                counter = int(data[5])
            else:
                counter = int(data[4])
        info = info.reset_index()
        if counter < info.shape[0]:
            reply = make_reply(data, info, counter)
        else:
            reply = make_err()
            bot.send_message(reply, chat_id)
            return
        bot.send_info(reply, data, counter, chat_id)

reqmnt_list = get_reqmnt_list()
state_list = []
city_list = []
plasma_type_list = []
plasma_donor_bloodgrp_list = []
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
                    if data[1] == 'Plasma':
                        plasma_type_list = get_plasma_type_list()
                    else:
                        state_list = get_state_list(data[1])
                elif data[0] == 'plasma_type':
                    city_list = get_plasma_city_list(data[2])
                elif data[0] == 'state':
                    city_list = get_city_list(data[1], data[2])
                elif data[0] == 'city' and data[1] == 'Plasma' and data[2] == 'Donors':
                    plasma_donor_bloodgrp_list = get_plasma_donor_bloodgrp_list(data[3])
                answer_query(data, reqmnt_list, state_list, city_list, plasma_type_list, plasma_donor_bloodgrp_list, from_, message_id, callback_id)
            elif 'message' in item:
                item = item['message']
                from_ = item['from']['id']
                reply = make_intro()
                bot.send_message(reply, from_)
                reply = make_reply()
                bot.send_message_inline(reply, 'reqmnt', reqmnt_list, from_)
