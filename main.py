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
  msgText = update.message.text.replace("/add ", "")
  if (Error.error(msgText)):
     bot.send_message(chat_id=update.message.chat_id, text = "Error in Adding! Try Again!",
                    parse_mode="Markdown")
  else:
    eventName = LogicHandler.stringToFn(Parser.textToLogic(msgText))
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with this format:DD/MM/YY HH:MM Location",
                    parse_mode="Markdown")
    
def collectMsg(bot, update):
    

addHandler = CommandHandler('add', addInput)

dispatcher.add_handler(addHandler)
updater.start_polling()
