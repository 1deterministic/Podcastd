import sqlite3

import config

def connect():
    try:
        handle = sqlite3.connect(config.database_file)
        handle.cursor().executescript(open(config.database_code, "r").read())
        handle.commit()

        return handle
    
    except:
        return None


def add_feed(target):
    try:
        handle = connect()
        if handle == None:
            return False

        handle.cursor().execute("insert or ignore into 'feed' (title, link, number, folder) values (?, ?, ?, ?);", (target["title"], target["link"], target["number"], target["folder"], ))
        handle.commit()

        return True

    except:
        return False


def get_feed(target):
    try:
        handle = connect()
        if handle == None:
            return []

        results = []
        for row in handle.cursor().execute("select * from 'feed' where title = ?;", (target["title"], )).fetchall():
            results.append({
                "title": row[0],
                "link": row[1],
                "number": row[2],
                "folder": row[3]
            })

        return results

    except:
        return []


def search_feed(target):
    try:
        handle = connect()
        if handle == None:
            return []

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

    except:
        return []


def find_feed(target):
    try:
        handle = connect()
        if handle == None:
            return []

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

    except:
        return []


def update_feed(target, changes):
    try:
        handle = connect()
        if handle == None:
            return False

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
        handle.commit()

        return True
    
    except:
        return False


def remove_feed(target):
    try:
        handle = connect()
        if handle == None:
            return False

        # handle.cursor().execute("delete from 'episode' where feed = ?;", (target["title"], ))
        handle.cursor().execute("delete from 'feed' where title = ?;", (target["title"], ))
        handle.commit()

        return True
    
    except:
        return False


def add_episode(target):
    try:
        handle = connect()
        if handle == None:
            return False

        handle.cursor().execute("insert or ignore into 'episode' (feed, title, date, link, file) values (?, ?, ?, ?, ?);", (target["feed"], target["title"], target["date"], target["link"], target["file"], ))
        handle.commit()

        return True
    
    except:
        return False


def get_episode(target):
    try:
        handle = connect()
        if handle == None:
            return []

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

    except:
        return []


def search_episode(target):
    try:
        handle = connect()
        if handle == None:
            return []

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

    except:
        return []


def find_episode(target):
    try:
        handle = connect()
        if handle == None:
            return []
            
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
    
    except:
        return []


def update_episode(target, changes):
    try:
        handle = connect()
        if handle == None:
            return False

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
        handle.commit()

        return True

    except:
        return False


def remove_episode(target):
    try:
        handle = connect()
        if handle == None:
            return False

        handle.cursor().execute("delete from 'episode' where feed = ? and title = ?;", (target["feed"], target["title"], ))
        handle.commit()

        return True
    
    except:
        return False