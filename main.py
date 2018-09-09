from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from add_meeting import *
from credentials import api_key
from helpers import *
from ping_users import user_handler
from db_manager import create_db, add_user

print("Bot started.") # Init message.

bot = get_bot()
updater = Updater(token=api_key)
dispatcher = updater.dispatcher

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

button_list = [
    InlineKeyboardButton("Talk to me before you reply this message!", url="t.me/u_l8_m8_bot")
]
reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))

def start_callback(bot, update):
    if (update.message.chat_id < 0):
        bot.send_message(chat_id=update.message.chat_id, text="Hello! Click start to allow me to pm you", reply_markup=reply_markup)
    else:
        username = update.message.from_user.username
        if username is none:
            bot.send_message(chat_id=update.message.chat_id, text="You need to set a username to use this bot. Set and start again.")
        else:    
            greeting = "Hello {}, you've been successfully added to u-l8-m8-bot!".format(username)
            add_chat_id_to_user(update.message.chat_id, update.message.from_user.username)
            bot.send_message(chat_id=update.message.chat_id, text=greeting)

start_handler = CommandHandler("start", start_callback)

# Add Start handler
dispatcher.add_handler(start_handler)

# Add Meeting handler
dispatcher.add_handler(add_meeting_handler)

# Add User handler
dispatcher.add_handler(user_handler)

# Add RSVP handlers
dispatcher.add_handler(rsvp_handler)
dispatcher.add_handler(end_rsvp_handler)

# Start up
open('state.txt', "w+").write('WAITING')
create_db()
print("init success")
updater.start_polling()
