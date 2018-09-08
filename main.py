from telegram.ext import Updater

from credentials import api_key
from helpers import *
from add_meeting import *
from ping_users import user_handler

bot = get_bot()
updater = Updater(token=api_key)
dispatcher = updater.dispatcher

# Add Meeting handler
dispatcher.add_handler(add_meeting_handler)

# Add User handler
dispatcher.add_handler(user_handler)

# Start up
updater.start_polling()
print("Bot started.") # Init message.
