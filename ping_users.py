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
    chat_id = get_chat_id_of_user(username)
    bot.send_message(chat_id, msg, reply_markup=ReplyKeyboardMarkup([[location_button]]))
    print("Message sent")

def determine_if_user_being_late(bot, update):
    print('start determine_if_user_being_late')
    username = update.message.from_user.username
    location = update.message.location
    print('determine_if_user_being_late 1')
    meeting_id = db_manager.find_user_latest_meeting(username)
    print('determine_if_user_being_late 2')
    travel_time = maps_api.get_travel_time(meeting_id, location)
    print('determine_if_user_being_late 3')
    travel_time *= 60
    print('determine_if_user_being_late 4')
    meeting_time = db_manager.get_meeting_time(meeting_id)
    print('determine_if_user_being_late 5')
    if travel_time > (meeting_time - int(time.time())):
        db_manager.update_is_late(meeting_id, username, True)
    print('end determine_if_user_being_late')


user_handler = MessageHandler(Filters.location, callback=determine_if_user_being_late)
