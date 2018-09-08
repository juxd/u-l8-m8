from credentials import api_key
from init import *
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters

# Set up bot to start listening.
bot = get_bot()
updater = Updater(token=api_key)
updater.start_polling()
print("Bot started.") # Init message.
