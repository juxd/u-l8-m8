from telegram.ext import MessageHandler, CommandHandler, Filters

WAITING_DATE, WAITING_LOCATION = range(2)

def add_meeting(bot, update):
    event_name = update.message.text.replace("/add ", "")
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with the meeting's date in this format: DD/MM/YY",
                    parse_mode="Markdown")
    return WAITING_DATE

def input_date(bot, update):
    date = update.message.text
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with the meeting's time in this format: HH:MM",
                parse_mode="Markdown")
    return WAITING_LOCATION

def input_location(bot, update):
    #somehow get one location
    location = update.message.location 
    return

add_meeting_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add_meeting)],
    states={
        WAITING_DATE: [MessageHandler(Filters.reply, input_date)],
        WAITING_LOCATION: [MessageHandler(Filters.reply, input_location)]
    },
    fallbacks=[CommandHandler('add', add_meeting)]
)
