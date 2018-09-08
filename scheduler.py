import sched, datetime
from ping_users import ping_for_loc
from reply_suggestions import reply_suggestions
from apscheduler.schedulers.background import BackgroundScheduler

s = BackgroundScheduler()
s.start()

def schedule_meeting_reminder(bot, meeting_id, time):
    print("scheduling")
    thirty_mins_before = time - 60 * 30

    twenty_five_mins_before = time - 60 * 25
    job = s.add_job(ping_for_loc, trigger='date', args=(bot, meeting_id), run_date=datetime.datetime.fromtimestamp(thirty_mins_before))
    job = s.add_job(reply_suggestions, trigger='date', args=(bot, meeting_id), run_date=datetime.datetime.fromtimestamp(twenty_five_mins_before))
