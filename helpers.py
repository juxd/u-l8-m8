import telegram
from credentials import api_key

def get_bot():
    bot = telegram.Bot(token=api_key)
    return bot

def test_bot(user_id):
    get_bot().send_message(chat_id=user_id, text='Hello World!')
