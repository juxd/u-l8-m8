from credentials import api_key
from helpers import *
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters

# Set up bot to start listening.
bot = get_bot()
updater = Updater(token=api_key)
updater.start_polling()

# Init message
print("Bot started.") 
