from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler
from dateutil import parser
import datetime

from db_manager import create_meeting
from scheduler import schedule_meeting_reminder

WAITING_DATE, WAITING_TIME, WAITING_LOCATION = range(3)

def add_meeting(bot, update, chat_data):
    print("start add_meeting")
    print("update file state:", "CREATING_MEETING")
    t = update.message.text.replace("/add ", "")
    chat_data['event_name'] = t
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with the meeting's date in this format: DDMMYY",
                    parse_mode="Markdown")
    return WAITING_DATE

def input_date(bot, update, chat_data):
    print("start input_date")
    chat_data['meeting_date'] = update.message.text
    print('date:', update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with the meeting's time in this format: HHMM",
                parse_mode="Markdown")
    return WAITING_TIME

def input_time(bot, update, chat_data):
    print("start input_time")
    chat_data['meeting_time'] = update.message.text
    print('time:', update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with attachment of the location",
                parse_mode="Markdown")
    return WAITING_LOCATION

def input_location(bot, update, chat_data):
    print("go fuck yourself")
    chat_data['longitude'] = update.message.location.longitude
    chat_data['latitude'] = update.message.location.latitude
    bot.send_message(chat_id=update.message.chat_id, text = "Reply this message with /rsvp to join and /end when done",
                parse_mode="Markdown")
    # Hand over control to a CommandHandler
    open('state.txt', "w+").write('RSVP')
    return -1

# Inserts meeting into database according to chat_data.
# Returns (meeting_id, seconds_since_epoch)
def insert_meeting(chat_id, chat_data):
    print(chat_data)
    print("start insert_meeting")
    # convert into MM/DD
    date_string = chat_data.get('meeting_date')[2:4] + '/' + chat_data.get('meeting_date')[0:2]
    time_string = chat_data.get('meeting_time')[0:2] + ':' + chat_data.get('meeting_time')[2:4]
    date = parser.parse(date_string + ' ' + time_string)
    epoch = datetime.datetime.utcfromtimestamp(0) 
    seconds_since_epoch = int((date - epoch).total_seconds())
    meeting_id = create_meeting(chat_id, seconds_since_epoch, chat_data.get('longitude'), chat_data.get('latitude'), chat_data.get('attendees'))
    return (meeting_id, seconds_since_epoch)

add_meeting_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add_meeting, pass_chat_data=True)],
    states={
        WAITING_DATE: [MessageHandler(Filters.reply, input_date, pass_chat_data=True)],
        WAITING_TIME: [MessageHandler(Filters.reply, input_time, pass_chat_data=True)],
        WAITING_LOCATION: [MessageHandler(Filters.reply, input_location, pass_chat_data=True)]
    },
    fallbacks=[CommandHandler('add', add_meeting)]
)

def input_rsvp(bot, update, chat_data):
    print("rsvp checking")
    if open('state.txt', "r").read() != 'RSVP':
        print("not in rsvp state, stopping input_rsvp")
        return
    print("rsvp received")
    if chat_data['attendees'] == None:
        chat_data['attendees'] = []
    chat_data.get('attendees').append(update.message.from_user.username)

def end_rsvp(bot, update, chat_data):
    print("checking end_rsvp")
    if open('state.txt', "r").read() != 'RSVP':
        print("not in rsvp state, stopping end_rsvp")
    print("starting end_rsvp")
    chat_id = update.message.chat_id
    meeting_id, seconds_since_epoch = insert_meeting(chat_id, chat_data)
    print("finish insert_meeting")
    schedule_meeting_reminder(bot, meeting_id, seconds_since_epoch)
    print("finish schedule_meeting_reminder")
    open('state.txt', "w+").write('WAITING')
    print("finish writing WAITING")
    print("end end_conversation")


rsvp_handler = CommandHandler("rsvp", input_rsvp, pass_chat_data=True)
end_rsvp_hanlder = CommandHandler("end", end_rsvp, pass_chat_data=True)
