import sched, datetime, time
from ping_users import ping_for_loc
from reply_suggestions import reply_suggestions
from apscheduler.schedulers.background import BackgroundScheduler


s = BackgroundScheduler()
s.start()

def schedule_meeting_reminder(bot, meeting_id, time):
    print("scheduling")
    thirty_mins_before = int(time.time()) + 5

    twenty_five_mins_before = int(time.time()) + 30
    print('dt:', datetime.datetime.fromtimestamp(thirty_mins_before))
    job = s.add_job(ping_for_loc, trigger='date', args=(bot, meeting_id), run_date=datetime.datetime.fromtimestamp(thirty_mins_before))
    job = s.add_job(reply_suggestions, trigger='date', args=(bot, meeting_id), run_date=datetime.datetime.fromtimestamp(twenty_five_mins_before))
