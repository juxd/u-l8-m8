from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler
from dateutil import parser
import datetime

from db_manager import create_meeting

WAITING_DATE, WAITING_TIME, WAITING_LOCATION = range(3)

def add_meeting(bot, update, chat_data):
    t = update.message.text.replace("/add ", "")
    chat_data['event_name'] = t
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with the meeting's date in this format: DDMMYY",
                    parse_mode="Markdown")
    return WAITING_DATE

def input_date(bot, update, chat_data):
    chat_data['meeting_date'] = update.message.text
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with the meeting's time in this format: HHMM",
                parse_mode="Markdown")
    return WAITING_TIME

def input_time(bot, update, chat_data):
    chat_data['meeting_time'] = update.message.text
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with attachment of the location",
                parse_mode="Markdown")
    return WAITING_LOCATION

def input_location(bot, update, chat_data):
    chat_data['longitude'] = update.message.location.longitude
    chat_data['latitude'] = update.message.location.latitude
    process_info(bot, update, chat_data)
    return

def process_info(bot, update, chat_data):
    chat_id = update.message.chat_id
    seconds_since_epoch = insert_meeting(chat_id, chat_data)
    schedule_meeting_reminder(bot, meeting_id, seconds_since_epoch)

# Inserts meeting into database according to chat_data.
# Returns seconds_since_epoch of the meeting time.
def insert_meeting(chat_id, chat_data):
    # convert into MM/DD
    date_string = chat_data.get('meeting_date')[2:4] + '/' + chat_data.get('meeting_date')[0:2]
    time_string = chat_data.get('meeting_time')[0:2] + ':' + chat_data.get('meeting_time')[2:4]
    date = parser.parse(date_string + ' ' + time_string)
    epoch = datetime.datetime.utcfromtimestamp(0) 
    seconds_since_epoch = int((date - epoch).total_seconds())
    create_meeting(chat_id, seconds_since_epoch, chat_data.get('longitude'), chat_data.get('latitude'), [])
    return seconds_since_epoch

add_meeting_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add_meeting, pass_chat_data=True)],
    states={
        WAITING_DATE: [MessageHandler(Filters.reply, input_date, pass_chat_data=True)],
        WAITING_TIME: [MessageHandler(Filters.reply, input_time, pass_chat_data=True)],
        WAITING_LOCATION: [MessageHandler(Filters.reply, input_location, pass_chat_data=True)]
    },
    fallbacks=[CommandHandler('add', add_meeting)]
)
