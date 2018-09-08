from credentials import api_key
from helper import *
import logging
from telegram.ext import Updater
from telegram.ext import MessageHandler, CommandHandler, Filters

# Set up bot to start listening.
bot = telegram.Bot(token=api_key)
updater = Updater(token=api_key)
dispatcher = updater.dispatcher
print("Bot started.") # Init message.


def addInput(bot, update):
    eventName = update.message.text.replace("/add ", "")
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with the meeting's date in this format: DD/MM/YY",
                    parse_mode="Markdown")
    dispatcher.add_handler(dateHandler)

def collectDate(bot, update):
    date = update.message.text;
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with the meeting's time in this format: HH:MM",
                parse_mode="Markdown")
    dispatcher.add_handler(timeHandler)
    
def collectTime(bot, update):
    time = update.message.text;
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with the location of meeting",
                parse_mode="Markdown")
    dispatcher.add_handler(locationHandler)

def collectLocation(bot, update):
    #somehow get one location
    #location = 

addHandler = CommandHandler('add', addInput)
dateHandler = MessageHandler(Filters.reply, collectDate)
timeHandler = MessageHandler(Filters.reply, collectTime)
locationHandler = MessageHandler(Filters.reply, collectLocation)

dispatcher.add_handler(addHandler)
updater.start_polling()
