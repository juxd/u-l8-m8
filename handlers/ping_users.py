import db
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Filters

def ping_for_loc(bot, meeting_id):
    people_ids = db.get_users_for_meeting(meeting_id)
    for person_id in people_ids:
        user_id = db.get_user_id(person_id)
        dispatcher_for_user = Dispatcher(bot)
        send_ping_to_person(dispatcher_for_user, user_id, meeting_id)

def send_ping_to_person(dispatcher, user_id, meeting_id):
    location_button = KeyboardButton("Send Location", request_location=True)
    msg = "Where u @ my nibba?"
    bot.send_message(user_id, msg, reply_markup=ReplyKeyboardMarkup([location_button]))
    userHandler = MessageHandler(Filters.location, callback=lambda bot, update: store_location(chat_id, update.message)))

def store_location(user_id, message, meeting_id):
    if chat_id != update.message.chat_id
        return
    db.store_location(user_id, message, meeting_id, message.location)

