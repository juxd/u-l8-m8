import db_manager
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Filters

user_handler = MessageHandler(Filters.location, callback=store_location)

def ping_for_loc(bot, meeting_id):
    people_ids = db_manager.get_meeting_people_id(meeting_id)
    for person_id in people_ids:
        user_id = db_manager.get_meeting_id(person_id)
        dispatcher_for_user = Dispatcher(bot)
        send_ping_to_person(dispatcher_for_user, user_id, meeting_id)

def send_ping_to_person(dispatcher, user_id, meeting_id):
    location_button = KeyboardButton("Send Location", request_location=True)
    msg = "Where u @ my nibba?"
    bot.send_message(user_id, msg, reply_markup=ReplyKeyboardMarkup([location_button]))

def store_location(bot, update):
    user_id = update.message.from_user.id
    meeting_id = db_manager.get_latest_meeting(user_id)
    db_manager.store_location(user_id, message, meeting_id, message.location)

