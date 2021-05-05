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
        r = requests.get(url, params=params)
        return r.json()
    
    def send_message(self, msg, chat_id):
        url = self.base + 'sendMessage'
        inline_keyboard = json.dumps({'inline_keyboard' : [[{'text' : "Here's how the Inline Keyboard works", 'url' : 'https://core.telegram.org/bots#inline-keyboards-and-on-the-fly-updating'}]]})
        params = {'chat_id' : chat_id, 'text' : msg, 'reply_markup' : inline_keyboard}
        if msg is not None:
            requests.post(url, data=params)
    
    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')
