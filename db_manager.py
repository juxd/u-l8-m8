import sqlite3
import time
DB_NAME = "meeting.db"


def create_db():
    # to be run when the bot initiate for the first time to create all the necessary db tables
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("""CREATE TABLE meetingTab 
        (meeting_id INTEGER PRIMARY KEY, meeting_time INTEGER, meeting_location_latitude REAL, 
        meeting_location_longitude REAL, group_id INTEGER)""")

        c.execute("""CREATE TABLE inTab
        (meeting_id INTEGER, username TEXT, chat_id INTEGER, is_late INTEGER)""")

        c.execute("""CREATE TABLE userTab
        (username TEXT UNIQUE, chat_id INTEGER, latest_location_latitude REAL, latest_location_longitude REAL)""")

        conn.commit()
        conn.close()
    except Exception as e:
        print (str(e))
        return False


def create_meeting(group_id, meeting_time, latitude, longitude, username_list):
    # given the parameters, this function creates a meeting in meetingTab and returns the autoincremented meeting_id
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""INSERT INTO meetingTab (group_id, meeting_time, meeting_location_latitude, meeting_location_longitude) 
        VALUES(?,?,?,?)""", (group_id, meeting_time, latitude, longitude))
        meeting_id = c.lastrowid

        for people in username_list:
            c.execute("INSERT INTO inTab (meeting_id, username, is_late) VALUES (?,?,?)", (meeting_id, people, 0))
        conn.commit()
        conn.close()
        return meeting_id

    except Exception as e:
        print (str(e))
        return False


def add_user_to_meeting(meeting_id, username):
    # add a user to an existing meeting based on meeting_id and username
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        param = (meeting_id, username, 0)
        c.execute("INSERT INTO inTab (meeting_id, username, is_late) VALUES (?,?,?)", param)

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(str(e))
        return False


# def add_chat_id_to_user(chat_id, username):
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     param = (chat_id, username)
#     c.execute("UPDATE inTab SET chat_id = ? WHERE username = ?", param)
#     conn.close()
#
# def get_chat_id_of_user(username):
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#
#     c.execute("SELECT chat_id FROM inTab WHERE username=?", username)
#     chat_id = c.fetchone()[0]
#     conn.close()
#     return chat_id

def get_meeting_time(meeting_id):
    # returns meeting time in unix time give meeting id
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        meeting_id = (meeting_id,)

        c.execute("SELECT meeting_time FROM meetingTab WHERE meeting_id=?", meeting_id)
        meeting_time = c.fetchone()[0]
        conn.close()

        return meeting_time
    except Exception as e:
        print (str(e))
        return False


def get_meeting_location(meeting_id):
    # returns meeting location in a tuple (lat, long) given meeting id
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        meeting_id = (meeting_id,)

        c.execute("SELECT meeting_location_latitude, meeting_location_longitude FROM meetingTab WHERE meeting_id=?", meeting_id)
        meetingLocation = c.fetchone()
        conn.close()

        return meetingLocation
    except Exception as e:
        print (str(e))
        return False


def get_meeting_group_id(meeting_id):
    # returns the group chat id based on meeting id
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        meeting_id = (meeting_id,)

        c.execute("SELECT group_id FROM meetingTab WHERE meeting_id=?", meeting_id)
        group_id = c.fetchone()[0]
        conn.close()

        return group_id
    except Exception as e:
        print (str(e))
        return False


def get_meeting_username(meeting_id):
    # returns a list of username of people involved in a meeting
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        meeting_id = (meeting_id, )
        c.execute("SELECT username FROM inTab WHERE meeting_id=?", meeting_id)
        username = c.fetchall()
        username_list = []
        for people in username:
            username_list.append(people[0])
        conn.close()

        return username_list
    except Exception as e:
        print (str(e))
        return False


def get_is_late(meeting_id, username):
    # returns a bool indicating whether a user is going to be late to a specific meeting
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        param = (meeting_id, username)
        c.execute("SELECT is_late FROM inTab WHERE meeting_id=? AND username=?", param)
        is_late = c.fetchone()[0]
        conn.close()
        if is_late == 1:
            return True
        else:
            return False

    except Exception as e:
        print(str(e))


def update_is_late(meeting_id, username, is_late):
    # update if a user is going to be late, provided the meeting_id and username
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        if is_late:
            late = 1
        else:
            late = 0

        param = (late, meeting_id, username)
        c.execute("UPDATE inTab SET is_late=? WHERE meeting_id=? AND username=?", param)

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(str(e))
        return False


def add_user(username, chat_id, latitude=None, longitude=None):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        param = (username, chat_id, latitude, longitude)

        c.execute("""REPLACE INTO userTab(username, chat_id, latest_location_latitude, latest_location_longitude) 
        VALUES (?,?,?,?)""", param)

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(str(e))
        return False


def get_user_chat_id(username):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        param = (username,)

        c.execute("SELECT chat_id FROM userTab WHERE username=?", param)

        chat_id = c.fetchone()[0]
        conn.close()
        return chat_id
    except Exception as e:
        print(str(e))
        return False


def update_user_location(username, latitude, longitude):
    try:
        chat_id = get_user_chat_id(username)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        param = (username, chat_id, latitude, longitude)
        
        c.execute("""REPLACE INTO userTab(username, chat_id, latest_location_latitude, latest_location_longitude) 
        VALUES (?,?,?,?)""", param)
        conn.commit()
        conn.close()

    except Exception as e:
        print(str(e))
        return False


def find_user_latest_location(username):
    # get a user's latest location, in tuple (lat, long)
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        param = (username, )

        c.execute("SELECT latest_location_latitude, latest_location_longitude FROM userTab WHERE username=?", param)
        location = c.fetchone()
        conn.close()
        return location
    except Exception as e:
        print(str(e))
        return False


def find_user_latest_meeting(username):
    # get the meeting_id of the meeting that is closest to the user on the timeline in the near future
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        now = int(time.time())
        param = (username,)

        c.execute("SELECT meeting_id FROM inTab WHERE username=?", param)
        meeting_id_list = c.fetchall()
        meeting_id_tuple = tuple()
        for m in meeting_id_list:
            meeting_id_tuple += m

        second_param = meeting_id_tuple + (now,)
        query = "SELECT meeting_id FROM meetingTab WHERE meeting_id IN ({}) AND meeting_time>? ORDER BY meeting_time ASC".format(
        ','.join('?'*len(meeting_id_tuple)))
        c.execute(query, second_param)
        meeting = c.fetchone()

        conn.close()

        return meeting

    except Exception as e:
        print (str(e))
        return False

# create_db()
# create_meeting(1,1,1,1,['a','b','c'])
#
# get_meeting_time(1)
# get_meeting_location(1)
# get_meeting_group_id(1)
# get_meeting_username(1)
#
# add_user_to_meeting(1,"d")
# get_is_late(1,'a')
# update_is_late(1,'a',True)
# get_is_late(1,'a')
#
# add_user('b', 1)
# update_user_location('b',1,1)
# find_user_latest_location('b')
# update_user_location('b',2,2)
# find_user_latest_location('b')
# find_user_latest_meeting('b')



add_user("c", 2)