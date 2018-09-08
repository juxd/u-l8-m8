import sched, time
import ping_users

def schedule_meeting_reminder(bot, meeting_id, time):
    s = sched.scheduler()
    thirty_mins_before = time.time() - 60 * 30
    twenty_mins_before = time.time() - 60 * 20
    s.enterabs(thirty_mins_before, 1, ping_users.ping_for_loc, argument=(bot, meeting_id))
    s.enterabs(twnety_mins_before, 1, reply_suggestions, argument=(bot, meeting_id))
    s.run()
