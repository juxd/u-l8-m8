from credentials import api_key
from helper import *
import logging
from telegram.ext import Updater
from telegram.ext import MessageHandler, CommandHandler, Filters

def add_input(bot, update):
    event_name = update.message.text.replace("/add ", "")
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with the meeting's date in this format: DD/MM/YY",
                    parse_mode="Markdown")
    dispatcher.add_handler(date_handler)

def collect_date(bot, update):
    date = update.message.text
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with the meeting's time in this format: HH:MM",
                parse_mode="Markdown")
    dispatcher.add_handler(time_handler)
    
def collect_time(bot, update):
    time = update.message.text
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with the location of meeting",
                parse_mode="Markdown")
    dispatcher.add_handler(location_handler)

def collect_location(bot, update):
    #somehow get one location
    location = update.message.location 

# Set up bot to start listening.
bot = get_bot()
updater = Updater(token=api_key)
dispatcher = updater.dispatcher

add_handler = CommandHandler('add', add_input)
date_handler = MessageHandler(Filters.all, collect_date)
time_handler = MessageHandler(Filters.all, collect_time)
location_handler = MessageHandler(Filters.location, collect_location)

dispatcher.add_handler(add_handler)
updater.start_polling()
print("Bot started.") # Init message.
