# covid_selfhelp_chatbot
A COVID Self Help Chatbot which responds to the user’s COVID related queries from an online database for the official Telegram group for COVID emergencies in IIT Kanpur. 

It has been featured on the official [IIT Kanpur Self-Help Website for COVID](https://sites.google.com/view/iitk-self-help/chatbotiitk?authuser=0). You can try the bot on [Telegram](https://t.me/covid_selfhelp_chatbot). 

## Demo

https://user-images.githubusercontent.com/66573172/148454950-bc778eb2-2930-4ea1-be60-46bce52645cd.mp4

## Files

1. `bot.py` contains the code for the Telegram Bot API.  
2. `server.py` contains the code for the flows and the logic of the bot.  
3. `extract_data.py` extracts the data from an online database and saves it in CSV format.  
4. `load_data.py` contains the code for loading the data from the CSV files.  
5. `search_google.py` corrects typos and makes the names of states and cities uniform. 
