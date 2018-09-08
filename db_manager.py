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


def createMeeting(groupID, meetingTime, latitude, longitude, peopleIDList):
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

def getMeetingTime(meetingID):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        meetingID = (meetingID,)

        c.execute("SELECT meetingTime FROM meetingTab WHERE meetingID=?", meetingID)
        meetingTime = c.fetchone()[0]
        print(meetingTime)

        return meetingTime
    except Exception as e:
        print str(e)

# create_db()
# createMeeting(1,1,1,1,[1,2,3,4])
# getMeetingTime(2)