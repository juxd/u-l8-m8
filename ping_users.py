import db_manager
import maps_api
import time
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Filters, MessageHandler

def ping_for_loc(bot, meeting_id):
    print("pinging users")
    username_list = db_manager.get_meeting_username(meeting_id)
    for username in username_list:
        send_ping_to_person(bot, username, meeting_id)

def send_ping_to_person(bot, username, meeting_id):
    print("{} being pinged".format(username))
    location_button = KeyboardButton("Send Location", request_location=True)
    msg = "Where u @ my nibba?"
    bot.send_message(username, msg, reply_markup=ReplyKeyboardMarkup([location_button]))

def determine_if_user_being_late(bot, update):
    username = update.message.from_user.username
    location = update.message.location
    meeting_id = db_manager.find_user_latest_meeting(username)
    travel_time = maps_api.get_travel_time(meeting_id, location)
    travel_time *= 60
    meeting_time = db_manager.get_meeting_time(meeting_id)
    if travel_time > (meeting_time - int(time.time())):
        db_manager.update_is_late(meeting_id, username, True)


user_handler = MessageHandler(Filters.location, callback=determine_if_user_being_late)
