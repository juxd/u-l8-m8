import sqlite3

DB_NAME = "meeting.db"


def create_db():
    # to be run when the bot initiate for the first time to create all the necessary db tables
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("""CREATE TABLE meetingTab 
        (meetingID INTEGER PRIMARY KEY, meetingTime INTEGER, meetingLocationLatitude REAL, 
        meetingLocationLongitude REAL, groupID INTEGER)""")

        c.execute("""CREATE TABLE inTab 
        (meetingID INTEGER, peopleID INTEGER, isLate INTEGER)""")

        conn.commit()
        conn.close()
    except Exception as e:
        print str(e)


def create_meeting(groupID, meetingTime, latitude, longitude, peopleIDList):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""INSERT INTO meetingTab (groupID, meetingTime, meetingLocationLatitude, meetingLocationLongitude) 
        VALUES(?,?,?,?)""", (groupID, meetingTime, latitude, longitude))
        meetingID = c.lastrowid

        for people in peopleIDList:
            c.execute("INSERT INTO inTab (meetingID, peopleID, isLate) VALUES (?,?,?)", (meetingID, people, 0))
        conn.commit()
        conn.close()
        print (meetingID)

    except Exception as e:
        print str(e)


def get_meeting_time(meetingID):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        meetingID = (meetingID,)

        c.execute("SELECT meetingTime FROM meetingTab WHERE meetingID=?", meetingID)
        meetingTime = c.fetchone()[0]
        conn.close()
        print(meetingTime)

        return meetingTime
    except Exception as e:
        print str(e)


def get_meeting_location(meetingID):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        meetingID = (meetingID,)

        c.execute("SELECT meetingLocationLatitude, meetingLocationLongitude FROM meetingTab WHERE meetingID=?", meetingID)
        meetingLocation = c.fetchone()
        conn.close()
        print(meetingLocation)

        return meetingLocation
    except Exception as e:
        print str(e)


def get_meeting_groupID(meetingID):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        meetingID = (meetingID,)

        c.execute("SELECT groupID FROM meetingTab WHERE meetingID=?", meetingID)
        groupID = c.fetchone()[0]
        conn.close()
        print(groupID)

        return groupID
    except Exception as e:
        print str(e)

def get_meeting_peopleID(meetingID):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        meetingID = (meetingID, )
        c.execute("SELECT peopleID FROM inTab WHERE meetingID=?", meetingID)
        peopleID = c.fetchall()
        peopleIDList = []
        for people in peopleID:
            peopleIDList.append(people[0])
        conn.close()
        print(peopleIDList)

        return peopleIDList
    except Exception as e:
        print (str(e))


def get_isLate(meetingID, peopleID):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        param = (meetingID, peopleID)
        c.execute("SELECT isLate FROM inTab WHERE meetingID=? AND peopleID=?", param)
        isLate = c.fetchone()[0]
        conn.close()
        if isLate == 1:
            print (isLate)
            return True
        else:
            print (isLate)
            return False

    except Exception as e:
        print (str(e))


def update_isLate(meetingID, peopleID, isLate):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        if isLate:
            late = 1
        else:
            late = 0

        param = (late, meetingID, peopleID)
        c.execute("UPDATE inTab SET isLate=? WHERE meetingID=? AND peopleID=?", param)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(str(e))
        return False


# create_db()
# createMeeting(1,1,1,1,[1,2,3,4])
# get_meeting_time(2)
# get_meeting_location(2)
# get_meeting_groupID(2)
# get_meeting_peopleID(2)
# get_isLate(2,2)
# update_isLate(2,2,True)
# get_isLate(2,2)