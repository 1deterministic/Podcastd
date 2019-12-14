import sqlite3

def connect(database, sqlcode):
    try:
        connection = sqlite3.connect(database)
        connection.cursor().executescript(open(sqlcode, "r").read())
        connection.commit()
        return connection
    except Exception as e:
        print(e)
        return None

def addFeed(database, title, link, number, folder):
    try:
        database.cursor().execute(f"insert into feed (title, link, number, folder) values (?, ?, ?, ?);", (title, link, number, folder, ))
        database.commit()
        return True
    except Exception as e:
        print(e)
        return False

def getFeeds(database):
    try:
        results = database.cursor().execute(f"select * from feed;").fetchall()

        data = []
        for result in results:
            data.append({
                "title": result[0],
                "link": result[1],
                "number": result[2],
                "folder": result[3]
            })

        return data

    except Exception as e:
        print(e)
        return None

def getSpecificFeed(database, title):
    try:
        results = database.cursor().execute(f"select * from feed where title = ?;", (title, )).fetchall()

        data = []
        for result in results:
            data.append({
                "title": result[0],
                "link": result[1],
                "number": result[2],
                "folder": result[3]
            })

        return data

    except Exception as e:
        print(e)
        return None

def updateFeed(database, newtitle, newlink, newnumber, newfolder, title):
    try:
        database.cursor().execute(f"update feed set title = ?, link = ?, number = ?, folder = ? where title = ?;", (newtitle, newlink, newnumber, newfolder, title))
        database.commit()
        return True
    except Exception as e:
        print(e)
        return False

def deleteFeed(database, title):
    try:
        database.cursor().execute(f"delete from entry where feed = ?;", (title, ))
        database.cursor().execute(f"delete from feed where title = ?;", (title, ))
        database.commit()
        return True
    except Exception as e:
        print(e)
        return None

def addEntry(database, title, date, link, file, downloaded, feed):
    try:
        database.cursor().execute(f"insert into entry (title, date, link, file, downloaded, feed) values (?, ?, ?, ?, ?, ?);", (title, date, link, file, downloaded, feed, ))
        database.commit()
        return True
    except Exception as e:
        print(e)
        return False

def getEntries(database, feed):
    try:
        results = database.cursor().execute(f"select * from entry where feed = ? order by date desc;", (feed, )).fetchall()

        data = []
        for result in results:
            data.append({
                "title": result[0],
                "feed": result[1],
                "date": result[2],
                "link": result[3],
                "file": result[4],
                "downloaded": result[5]
            })

        return data
    
    except Exception as e:
        print(e)
        return None

def getSpecificEntriy(database, feed, title):
    try:
        results = database.cursor().execute(f"select * from entry where feed = ? and title = ?;", (feed, title, )).fetchall()

        data = []
        for result in results:
            data.append({
                "title": result[0],
                "feed": result[1],
                "date": result[2],
                "link": result[3],
                "file": result[4],
                "downloaded": result[5]
            })

        return data
    
    except Exception as e:
        print(e)
        return None

def updateEntry(database, newtitle, newdate, newlink, newfile, newdownloaded, newfeed, title, feed):
    try:
        database.cursor().execute(f"update entry set title = ?, date = ?, link = ?, file = ?, downloaded = ?, feed = ? where title = ? and feed = ?;", (newtitle, newdate, newlink, newfile, newdownloaded, newfeed, title, feed))
        database.commit()
        return True
    except Exception as e:
        print(e)
        return False

def deleteEntry(database, title, feed):
    try:
        database.cursor().execute(f"delete from entry where title = ? and feed = ?;", (title, feed, ))
        database.commit()
        return True
    except Exception as e:
        print(e)
        return None