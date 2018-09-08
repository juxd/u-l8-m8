import db_manager
import scheduler


def reply_suggestions(bot, meeting_id):
    users = db_manager.get_meeting_username(meeting_id)
    group_id = db_manager.get_meeting_group_id(meeting_id)

    on_time_list = [db_manager.get_is_late(meeting_id, u) for u in users]
    ratio_on_time = len(filter(lambda x: x == False, on_time_list)) / len(on_time_list)
    if ratio_on_time > 0.5:
       # Send group message that most people are on time.
        message = "Most of the people are on time, YAY! The meeting is happening!"
        bot.send_message(chat_id=group_id, text=message)

    else :
       # Send group message that they should reschedule.
        message = "Most of the people cannot make it. let us postpone the meeting"
        bot.send_message(chat_id=group_id, text=message)
        reschedule_meeting(bot, meeting_id)


def reschedule_meeting(bot, meeting_id):
    group_id = db_manager.get_meeting_group_id(meeting_id)
    location = db_manager.get_meeting_location(meeting_id)
    original_time = db_manager.get_meeting_time(meeting_id)
    new_time = original_time + 60 * 60
    usernames = db_manager.get_meeting_username(meeting_id)
    new_meeting_id = db_manager.create_meeting(group_id, new_time, location[0], location[1], usernames)
    scheduler.schedule_meeting_reminder(bot, meeting_id, new_time)
    bot.send_message(chat_id=group_id, text="meeting rescheduled to one hour later")

