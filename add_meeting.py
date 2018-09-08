from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler
from dateutil import parser

WAITING_DATE, WAITING_TIME, WAITING_LOCATION = range(3)

# Keep meeting information in memory
store = {
        'event_name': None,
        'meeting_time': None,
        'meeting_date': None,
        'lat': None,
        'lon': None
        }

def add_meeting(bot, update):
    store.set('event_name', update.message.text.replace("/add ", ""))
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with the meeting's date in this format: DDMMYY",
                    parse_mode="Markdown")
    return WAITING_DATE

def input_date(bot, update):
    store.set('meeting_date', update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with the meeting's time in this format: HHMM",
                parse_mode="Markdown")
    return WAITING_TIME

def input_time(bot, update):
    store.set('meeting_time', update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with attachment of the location",
                parse_mode="Markdown")
    return WAITING_LOCATION

def input_location(bot, update):
    store.set('longitude', update.message.location.longitude)
    store.set('lantitude', update.message.location.latitude)
    insert_meeting(update.message.chat.id)
    return

def insert_meeting(chat_id):
    # convert into MM/DD
    date_string = store.get('meeting_date')[2:4] + '/' + store.get('meeting_date')[0:2]
    time_string = store.get('meeting_time')[0:2] + ':' + store.get('meeting_time')[2:4]
    date = parser.parse(date_string + ' ' + time_string)
    epoch = datetime.datetime.utcfromtimestamp(0) 
    seconds_since_epoch = int((date - epoch).total_seconds())

    create_meeting(chat_id, seconds_since_epoch, store.get('lon'), store.get('lat'), [])


add_meeting_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add_meeting)],
    states={
        WAITING_DATE: [MessageHandler(Filters.reply, input_date)],
        WAITING_TIME: [MessageHandler(Filters.reply, input_time)],
        WAITING_LOCATION: [MessageHandler(Filters.reply, input_location)]
    },
    fallbacks=[CommandHandler('add', add_meeting)]
)
