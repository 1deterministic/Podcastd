import os
import urllib.parse
import requests
import feedparser
import dateutil.parser

import defaults
import database

def doList(db, target):
    if db is None or target is None:
        return False
    
    try:
        if "title" in target.keys():
            feeds = database.getSpecificFeed(db, target["title"])
        else:
            feeds = database.getFeeds(db)

        print(feeds)
        return True

    except:
        return False

def doUpdate(db, target):
    if db is None or target is None:
        return False

    try:
        if "title" in target.keys():
            feeds = database.getSpecificFeed(db, target["title"])
        else:
            feeds = database.getFeeds(db)
            
        for feed in feeds:
            rss = feedparser.parse(feed["link"])
            for entry in rss.entries:
                for link in entry.links:
                    if link.type.startswith("audio"):
                        database.addEntry(db, entry.title, int(dateutil.parser.parse(entry.published).timestamp()), link.href, "", "False", feed["title"])

        return True

    except:
        return False

def doAdd(db, target):
    if db is None or target is None or not "link" in target.keys():
        return False

    try:
        rss = feedparser.parse(target["link"])
        database.addFeed(db, target["title"] if "title" in target.keys() else rss.feed.title, target["link"], target["number"] if "number" in target.keys() else defaults.NUMBER, target["folder"] if "folder" in target.keys() else os.path.join(defaults.FOLDER, rss.feed.title))

        return True

    except:
        return False

def doModify(db, target, changes):
    if db is None or target is None or not "title" in target.keys():
        return False

    try:
        feed = database.getSpecificFeed(db, target["title"])
        
        database.updateFeed(db, changes["title"] if "title" in changes.keys() else feed[0]["title"], changes["link"] if "link" in changes.keys() else feed[0]["link"], changes["number"] if "number" in changes.keys() else feed[0]["number"], changes["folder"] if "folder" in changes.keys() else feed[0]["folder"], feed[0]["title"])

        return True

    except:
        return False

def doRemove(db, target):
    if db is None or target is None or not "title" in target.keys():
        return False

    try:
        database.deleteFeed(db, target["title"])

        return True

    except:
        return False

def doDownload(db, target):
    if db is None or target is None:
        return False
    
    try:
        if "title" in target.keys():
            feeds = database.getSpecificFeed(db, target["title"])
        else:
            feeds = database.getFeeds(db)

        for feed in feeds:
            if os.path.isdir(feed["folder"]) == False:
                os.mkdir(feed["folder"])
            
            downloaded = 0
            entries = database.getEntries(db, feed["title"])
            for entry in entries:
                if entry["downloaded"] == "True":
                    downloaded += 1

                    if downloaded > feed["number"] and feed["number"] != -1:
                        print(f"Removing old episode: {entry['title']} ... ", end="")
                        os.remove(entry["file"])
                        database.updateEntry(db, entry["title"], entry["date"], entry["link"], "", "False", feed["title"], entry["title"], feed["title"])
                        downloaded += -1
                        print(f"Done!")
                    else:
                        print(f"Skipped downloaded episode: {entry['title']}")

                elif downloaded < feed["number"] or feed["number"] == -1:
                    print(f"Downloading new episode: {entry['title']} ... ", end="")
                    path = os.path.join(feed["folder"], entry["title"] + os.path.splitext(urllib.parse.urlparse(entry["link"]).path)[1])
                    req = requests.get(entry["link"])
                    open(path, "wb").write(req.content)
                    database.updateEntry(db, entry["title"], entry["date"], entry["link"], path, "True", feed["title"], entry["title"], feed["title"])
                    downloaded += 1
                    print(f"Done!")
        
        return True

    except:
        return False