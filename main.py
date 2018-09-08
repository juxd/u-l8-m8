from telegram.ext import Updater

from add_meeting import *
from credentials import api_key
from helpers import *
from ping_users import user_handler
from db_manager import create_db

bot = get_bot()
updater = Updater(token=api_key)
dispatcher = updater.dispatcher

# Add Meeting handler
dispatcher.add_handler(add_meeting_handler)

# Add User handler
dispatcher.add_handler(user_handler)

# Start up
create_db()
updater.start_polling()
print("Bot started.") # Init message.

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

button_list = [
    InlineKeyboardButton("Talk to me before you reply this message!", url = "https://telegram.me/u-l8-m8-bot")
]
reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
bot.send_message(chat_id=update.message.chat_id, "Hello! Click start to allow me to pm you", reply_markup=reply_markup)
