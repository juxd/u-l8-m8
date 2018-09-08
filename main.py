from credentials import api_key
from init import *
from telegram.ext import Updater
from telegram.ext import MessageHandler, CommandHandler, Filters

# Set up bot to start listening.
bot = telegram.Bot(token=config.token)
updater = Updater(token=config.token)
dispatcher = updater.dispatcher
print("Bot started.") # Init message.


def addInput(bot, update):
    eventName = update.message.text.replace("/add ", "")
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message in this format: DD/MM/YY HH:MM Location",
                    parse_mode="Markdown")
    dispatcher.add_handler(detailsHandler)

def collectDetails:
    details = update.message.text;
    detailsList = details.split(" ")
    date = detailsList[0]
    time = detailsList[1]
    place = detailsList[2]
    
addHandler = CommandHandler('add', addInput)
detailsHandler = MessageHandler(Filters.reply, collectDetails)

dispatcher.add_handler(addHandler)
updater.start_polling()
