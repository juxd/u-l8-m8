def reply_suggestions(bot, meeting_id):
    users = getUsersInMeeting(meeting_id)
    meeting_time = getMeetingTime(meeting_id)
    on_time_list = [isOnTime(u, meeting_id) for u in users] 
    ratio_on_time = len(filter(lambda x: x == True, on_time_list)) / len(on_time_list)
    if ratio_on_time > 0.5:
       # Send group message that most people are on time. 
    else :
       # Send group message that they should reschedule. 
