import db_manager
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Filters, MessageHandler

def ping_for_loc(bot, meeting_id):
    username_list = db_manager.get_meeting_username(meeting_id)
    for username in username_list:
        dispatcher_for_user = Dispatcher(bot)
        send_ping_to_person(dispatcher_for_user, username, meeting_id)

def send_ping_to_person(dispatcher, username, meeting_id):
    location_button = KeyboardButton("Send Location", request_location=True)
    msg = "Where u @ my nibba?"
    bot.send_message(username, msg, reply_markup=ReplyKeyboardMarkup([location_button]))

def store_location(bot, update):
    username = update.message.from_user.username
    location = update.message.location
    meeting_id = db_manager.find_user_latest_meeting(user_id)
    db_manager.update_user_location(username, location.latitude, location.longitude)

user_handler = MessageHandler(Filters.location, callback=store_location)
