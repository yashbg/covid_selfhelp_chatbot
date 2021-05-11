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
        
    def get_updates(self, offset=None):
        url = self.base + 'getUpdates'
        params = {'timeout': 100}
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
            [{'text': trim(option), 'callback_data': f'{option_type}:{trim(option)}'}] for option in option_list
        ]}
        params = {'chat_id': chat_id, 'text': msg, 'reply_markup': json.dumps(inline_keyboard)}
        requests.post(url, params)
    
    def send_info(self, msg, data, counter, chat_id):
        url = self.base + 'sendMessage'
        # data -> option_type:reqmnt:state:city:counter
        inline_keyboard = {'inline_keyboard': [
            [{'text': 'Show more', 'callback_data': f'end:{data[1]}:{data[2]}:{data[3]}:{counter + 1}'}]
        ]}
        params = {'chat_id': chat_id, 'text': msg, 'reply_markup': json.dumps(inline_keyboard)}
        requests.post(url, params)

    def edit_message(self, msg, option_type, option_list, chat_id, message_id, reqmnt=None, state=None):
        url = self.base + 'editMessageText'
        if option_type == 'reqmnt':
            inline_keyboard = {'inline_keyboard': [
                [{'text': option, 'callback_data': f'{option_type}:{option}:None:None'}] for option in option_list
            ]}
        elif option_type == 'state':
            inline_keyboard = {'inline_keyboard': [
                [{'text': option, 'callback_data': f'{option_type}:{reqmnt}:{option}:None'}] for option in option_list
            ]}
            inline_keyboard['inline_keyboard'].append([
                {'text': 'Back', 'callback_data': f'start:None:None:None'},
                {'text': 'Start Over', 'callback_data': f'start:None:None:None'},
            ])
        elif option_type == 'city':
            inline_keyboard = {'inline_keyboard': [
                [{'text': option, 'callback_data': f'{option_type}:{reqmnt}:{state}:{option}'}] for option in option_list
            ]}
            inline_keyboard['inline_keyboard'].append([
                {'text': 'Back', 'callback_data': f'reqmnt:{reqmnt}:None:None'},
                {'text': 'Start Over', 'callback_data': f'start:None:None:None'},
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
