import requests
import json
import configparser as cfg

def trim(str):
    str = (str[:50] + '..') if len(str) > 50 else str
    return str

class telegram_chatbot():
    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)
        
    def get_updates(self, offset=None, timeout=100):
        url = self.base + 'getUpdates'
        params = {'timeout': timeout}
        if offset:
            params['offset'] = offset + 1
        r = requests.get(url, params)
        return r.json()
    
    def send_message(self, msg, chat_id):
        url = self.base + 'sendMessage'
        params = {'chat_id': chat_id, 'text': msg}
        requests.post(url, params)

    def send_message_inline(self, msg, option_type, option_list, chat_id):
        url = self.base + 'sendMessage'
        inline_keyboard = {'inline_keyboard': [
            [{'text': trim(str(option)), 'callback_data': f'{option_type}:{option}'}] for option in option_list
        ]}
        params = {'chat_id': chat_id, 'text': msg, 'reply_markup': json.dumps(inline_keyboard)}
        requests.post(url, params)
    
    def send_info(self, msg, data, counter, chat_id):
        url = self.base + 'sendMessage'
        if data[1] == 'Medicines':
            # data -> option_type:reqmnt:state:counter
            inline_keyboard = {'inline_keyboard': [
                [{'text': 'Show more', 'callback_data': f'end:{data[1]}:{data[2]}:{counter + 1}'}]
            ]}
        elif data[0] == 'plasma_donor_bloodgrp' or (data[0] == 'end' and data[1] == 'Plasma' and data[2] == 'Donors'):
            # data -> option_type:reqmnt:type:city:bloodgrp:counter
            inline_keyboard = {'inline_keyboard': [
                [{'text': 'Show more', 'callback_data': f'end:{data[1]}:{data[2]}:{data[3]}:{data[4]}:{counter + 1}'}]
            ]}
        else:
            # data -> option_type:reqmnt:type:city:counter for Plasma (Organisations)
            # data -> option_type:reqmnt:state:city:counter otherwise
            inline_keyboard = {'inline_keyboard': [
                [{'text': 'Show more', 'callback_data': f'end:{data[1]}:{data[2]}:{data[3]}:{counter + 1}'}]
            ]}
        params = {'chat_id': chat_id, 'text': msg, 'reply_markup': json.dumps(inline_keyboard)}
        requests.post(url, params)

    def edit_message(self, msg, option_type, option_list, chat_id, message_id, reqmnt=None, state=None, plasma_type=None, city=None):
        url = self.base + 'editMessageText'
        if option_type == 'reqmnt':
            inline_keyboard = {'inline_keyboard': [
                [{'text': trim(str(option)), 'callback_data': f'{option_type}:{option}:None:None'}] for option in option_list
            ]}
        elif option_type == 'plasma_type':
            inline_keyboard = {'inline_keyboard': [
                [{'text': trim(str(option)), 'callback_data': f'{option_type}:{reqmnt}:{option}'}] for option in option_list
            ]}
            inline_keyboard['inline_keyboard'].append([
                {'text': 'Back', 'callback_data': f'start'},
                {'text': 'Start Over', 'callback_data': f'start'},
            ])
        elif option_type == 'state':
            inline_keyboard = {'inline_keyboard': [
                [{'text': trim(str(option)), 'callback_data': f'{option_type}:{reqmnt}:{option}:None'}] for option in option_list
            ]}
            inline_keyboard['inline_keyboard'].append([
                {'text': 'Back', 'callback_data': f'start:None:None:None'},
                {'text': 'Start Over', 'callback_data': f'start:None:None:None'},
            ])
        elif option_type == 'city':
            if reqmnt == 'Plasma':
                inline_keyboard = {'inline_keyboard': [
                    [{'text': trim(str(option)), 'callback_data': f'{option_type}:{reqmnt}:{plasma_type}:{option}'}] for option in option_list
                ]}
                inline_keyboard['inline_keyboard'].append([
                    {'text': 'Back', 'callback_data': f'reqmnt:{reqmnt}'},
                    {'text': 'Start Over', 'callback_data': f'start'},
                ])
            else:
                inline_keyboard = {'inline_keyboard': [
                    [{'text': trim(str(option)), 'callback_data': f'{option_type}:{reqmnt}:{state}:{option}'}] for option in option_list
                ]}
                inline_keyboard['inline_keyboard'].append([
                    {'text': 'Back', 'callback_data': f'reqmnt:{reqmnt}:None:None'},
                    {'text': 'Start Over', 'callback_data': f'start:None:None:None'},
                ])
        elif option_type == 'plasma_donor_bloodgrp':
            inline_keyboard = {'inline_keyboard': [
                [{'text': trim(str(option)), 'callback_data': f'{option_type}:{reqmnt}:{plasma_type}:{city}:{option}'}] for option in option_list
            ]}
            inline_keyboard['inline_keyboard'].append([
                {'text': 'Back', 'callback_data': f'plasma_type:{reqmnt}:{plasma_type}'},
                {'text': 'Start Over', 'callback_data': f'start'},
            ])
        params = {'chat_id': chat_id, 'message_id': message_id, 'text': msg, 'reply_markup': json.dumps(inline_keyboard)}
        requests.post(url, params)

    def answer_callback_query(self, callback_id):
        url = self.base + 'answerCallbackQuery'
        params = {'callback_query_id': callback_id}
        requests.post(url, params)
    
    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')
