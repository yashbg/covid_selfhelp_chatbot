import requests
import json
import configparser as cfg

class telegram_chatbot():
    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)
        
    def get_updates(self, offset=None):
        url = self.base + 'getUpdates'
        params = {'timeout' : 100}
        if offset:
            params['offset'] = offset + 1
        r = requests.get(url, params)
        return r.json()

    def send_message_inline(self, msg, chat_id):
        url = self.base + 'sendMessage'
        inline_keyboard = json.dumps({'inline_keyboard' : [
            [
                {'text' : '1', 'callback_data' : '1'},
                {'text' : '2', 'callback_data' : '2'},
            ],
            [
                {'text' : '3', 'callback_data' : '3'},
                {'text' : '4', 'callback_data' : '4'},
            ],
        ]})
        params = {'chat_id' : chat_id, 'text' : msg, 'reply_markup' : inline_keyboard}
        if msg is not None:
            requests.post(url, params)
    
    def send_message(self, msg, chat_id):
        url = self.base + 'sendMessage'
        params = {'chat_id' : chat_id, 'text' : msg}
        if msg is not None:
            requests.post(url, params)

    def answer_callback_query(self, callback_id):
        url = self.base + 'answerCallbackQuery'
        params = {'callback_query_id' : callback_id}
        requests.post(url, params)
    
    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')
