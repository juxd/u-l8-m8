import sched, time
import ping_users

def schedule_meeting_reminder(bot, meeting_id, time):
    thirty_mins_before = time.time() - 60 * 30
    twenty_mins_before = time.time() - 60 * 20
    sched.enterabs(thirty_mins_before, 1, ping_for_loc, argument=(bot, meeting_id))
    sched.enterabs(twnety_mins_before, 1, reply_suggestions, argument=(bot, meeting_id))
