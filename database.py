import sqlite3

path = "database.db"
code = "database.sql"

def connect(path, code):
    handle = sqlite3.connect(path)
    handle.cursor().executescript(open(code, "r").read())
    handle.commit()

    return handle


def add_feed(handle, target):
    handle.cursor().execute("insert or ignore into 'feed' (title, link, number, folder) values (?, ?, ?, ?);", (target["title"], target["link"], target["number"], target["folder"], ))
    return handle.commit()


def get_feed(handle, target):
    results = []

    for row in handle.cursor().execute("select * from 'feed' where title = ?;", (target["title"], )).fetchall():
        results.append({
            "title": row[0],
            "link": row[1],
            "number": row[2],
            "folder": row[3]
        })
    
    return results


def search_feed(handle, target):
    conditions = ""
    values = []

    if len(target.keys()) > 0:
        conditions = " where"
        first = True

        for key in target.keys():
            if not first:
                conditions += " and"

            conditions += f" {key} = ?"
            values.append(target[key])

            first = False

    results = []

    for row in handle.cursor().execute(f"select * from 'feed'{conditions} order by title desc;", (* values, )).fetchall():
        results.append({
            "title": row[0],
            "link": row[1],
            "number": row[2],
            "folder": row[3]
        })
    
    return results


def find_feed(handle, target):
    conditions = ""
    values = []

    if len(target.keys()) > 0:
        conditions = " where"
        first = True

        for key in target.keys():
            if not first:
                conditions += " or"

            conditions += f" {key} = ?"
            values.append(target[key])

            first = False

    results = []

    for row in handle.cursor().execute(f"select * from 'feed'{conditions} order by title desc;", (* values, )).fetchall():
        results.append({
            "title": row[0],
            "link": row[1],
            "number": row[2],
            "folder": row[3]
        })
    
    return results


def update_feed(handle, target, changes):
    conditions = ""
    values = []

    if len(target.keys()) > 0:
        conditions = " where"
        first = True

        for key in target.keys():
            if not first:
                conditions += " and"

            conditions += f" {key} = ?"
            values.append(target[key])

            first = False

    fields = ""
    new_values = []

    if len(changes.keys()) > 0:
        fields = " set"
        first = True

        for key in changes.keys():
            if not first:
                fields += ","

            fields += f" {key} = ?"
            new_values.append(changes[key])

            first = False

    handle.cursor().execute(f"update 'feed'{fields}{conditions};", (* new_values, * values, ))
    return handle.commit()


def remove_feed(handle, target):
    # handle.cursor().execute("delete from 'episode' where feed = ?;", (target["title"], ))
    handle.cursor().execute("delete from 'feed' where title = ?;", (target["title"], ))
    return handle.commit()


def add_episode(handle, target):
    handle.cursor().execute("insert or ignore into 'episode' (feed, title, date, link, file) values (?, ?, ?, ?, ?);", (target["feed"], target["title"], target["date"], target["link"], target["file"], ))
    return handle.commit()


def get_episode(handle, target):
    results = []

    for row in handle.cursor().execute("select * from 'episode' where feed = ? and title = ?;", (taget["feed"], target["title"], )).fetchall():
        results.append({
            "feed": row[0],
            "title": row[1],
            "date": row[2],
            "link": row[3],
            "file": row[4]
        })
    
    return results


def search_episode(handle, target):
    conditions = ""
    values = []

    if len(target.keys()) > 0:
        conditions = " where"
        first = True

        for key in target.keys():
            if not first:
                conditions += " and"

            conditions += f" {key} = ?"
            values.append(target[key])

            first = False

    results = []

    for row in handle.cursor().execute(f"select * from 'episode'{conditions} order by date desc;", (* values, )).fetchall():
        results.append({
            "feed": row[0],
            "title": row[1],
            "date": row[2],
            "link": row[3],
            "file": row[4]
        })
    
    return results


def find_episode(handle, target):
    conditions = ""
    values = []

    if len(target.keys()) > 0:
        conditions = " where"
        first = True

        for key in target.keys():
            if not first:
                conditions += " or"

            conditions += f" {key} = ?"
            values.append(target[key])

            first = False

    results = []

    for row in handle.cursor().execute(f"select * from 'episode'{conditions} order by date desc;", (* values, )).fetchall():
        results.append({
            "feed": row[0],
            "title": row[1],
            "date": row[2],
            "link": row[3],
            "file": row[4]
        })
    
    return results


def update_episode(handle, target, changes):
    conditions = ""
    values = []

    if len(target.keys()) > 0:
        conditions = " where"
        first = True

        for key in target.keys():
            if not first:
                conditions += " and"

            conditions += f" {key} = ?"
            values.append(target[key])

            first = False

    fields = ""
    new_values = []

    if len(changes.keys()) > 0:
        fields = " set"
        first = True

        for key in changes.keys():
            if not first:
                fields += ","

            fields += f" {key} = ?"
            new_values.append(changes[key])

            first = False

    handle.cursor().execute(f"update 'episode'{fields}{conditions};", (* new_values, * values, ))
    return handle.commit()


def remove_episode(handle, target):
    handle.cursor().execute("delete from 'episode' where feed = ? and title = ?;", (target["feed"], target["title"], ))
    return handle.commit()