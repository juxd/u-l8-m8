import sched, datetime
from ping_users import ping_for_loc
from reply_suggestions import reply_suggestions
from apscheduler.scheduler.background import BackgroundScheduler

def schedule_meeting_reminder(bot, meeting_id, time):
    print("scheduling")
    s = BackgroundScheduler()
    thirty_mins_before = time - 60 * 30

    twenty_five_mins_before = time - 60 * 25
    s.add_job(ping_for_loc, trigger='date', run_date=datetime.fromtimestamp(thirty_mins_before))
    # s.enterabs(thirty_mins_before, 1, ping_for_loc, argument=(bot, meeting_id))
    # s.enterabs(twenty_five_mins_before, 1, reply_suggestions, argument=(bot, meeting_id))
    s.start()
