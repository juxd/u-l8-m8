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
        (meeting_id INTEGER, people_id INTEGER, is_late INTEGER)""")

        c.execute("""CREATE TABLE userTab
        (people_id INTEGER UNIQUE, latest_location_latitude REAL, latest_location_longitude REAL)""")

        conn.commit()
        conn.close()
    except Exception as e:
        print (str(e))
        return False


def create_meeting(group_id, meeting_time, latitude, longitude, people_id_list):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""INSERT INTO meetingTab (group_id, meeting_time, meeting_location_latitude, meeting_location_longitude) 
        VALUES(?,?,?,?)""", (group_id, meeting_time, latitude, longitude))
        meeting_id = c.lastrowid

        for people in people_id_list:
            c.execute("INSERT INTO inTab (meeting_id, people_id, is_late) VALUES (?,?,?)", (meeting_id, people, 0))
        conn.commit()
        conn.close()
        return meeting_id

    except Exception as e:
        print (str(e))
        return False


def get_meeting_time(meeting_id):
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


def get_meeting_people_id(meeting_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        meeting_id = (meeting_id, )
        c.execute("SELECT people_id FROM inTab WHERE meeting_id=?", meeting_id)
        people_id = c.fetchall()
        people_id_list = []
        for people in people_id:
            people_id_list.append(people[0])
        conn.close()

        return people_id_list
    except Exception as e:
        print (str(e))
        return False


def get_is_late(meeting_id, people_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        param = (meeting_id, people_id)
        c.execute("SELECT is_late FROM inTab WHERE meeting_id=? AND people_id=?", param)
        is_late = c.fetchone()[0]
        conn.close()
        if is_late == 1:
            return True
        else:
            return False

    except Exception as e:
        print(str(e))


def update_is_late(meeting_id, people_id, is_late):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        if is_late:
            late = 1
        else:
            late = 0

        param = (late, meeting_id, people_id)
        c.execute("UPDATE inTab SET is_late=? WHERE meeting_id=? AND people_id=?", param)

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(str(e))
        return False


def update_user_location(people_id, latitude, longitude):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        param = (people_id, latitude, longitude)
        
        c.execute("""REPLACE INTO userTab(people_id, latest_location_latitude, latest_location_longitude) 
        VALUES (?,?,?)""", param)
        conn.commit()
        conn.close()

    except Exception as e:
        print(str(e))
        return False


def find_user_latest_location(people_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        param = (people_id, )

        c.execute("SELECT latest_location_latitude, latest_location_longitude FROM userTab WHERE people_id=?", param)
        location = c.fetchone()
        conn.close()
        return location
    except Exception as e:
        print(str(e))
        return False


def find_user_latest_meeting(people_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        now = int(time.time())
        param = (people_id,)

        c.execute("SELECT meeting_id FROM inTab WHERE people_id=?", param)
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
# create_meeting(1,1,1,1,[1,2,3,4])
# get_meeting_time(2)
# get_meeting_location(2)
# get_meeting_group_id(2)
# get_meeting_people_id(2)
# get_is_late(2,2)
# update_is_late(2,2,True)
# get_is_late(2,2)
#
# update_user_location(1,1,1)
# find_user_latest_location(1)
# update_user_location(1,2,2)
# find_user_latest_location(1)
# find_user_latest_meeting(1)

