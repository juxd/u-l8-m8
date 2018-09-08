import sched, time
from ping_users import ping_for_loc
from reply_suggestions import reply_suggestions

def schedule_meeting_reminder(bot, meeting_id, time):
    print("scheduling")
    s = sched.scheduler()
    thirty_mins_before = time - 60 * 30

    twenty_five_mins_before = time - 60 * 25
    s.enterabs(thirty_mins_before, 1, ping_for_loc, argument=(bot, meeting_id))
    s.enterabs(twenty_five_mins_before, 1, reply_suggestions, argument=(bot, meeting_id))
    s.run()
