import os
import json
import feedparser
import requests
import dateutil.parser
import urllib.parse
import subprocess
import threading

import database
import config

def list_feed(target):
    handle = database.connect(config.database_file, config.sql_file)

    print(json.dumps(database.search_feed(handle, target), indent = 2))

def add_feed(target):
    handle = database.connect(config.database_file, config.sql_file)

    # use defaults if not specified
    if not "number" in target.keys():
        target["number"] = config.default_number

    if not "folder" in target.keys():
        target["folder"] = os.path.join(config.default_root, target["title"])

    database.add_feed(handle, target)

def modify_feed(target, changes):
    handle = database.connect(config.database_file, config.sql_file)

    database.update_feed(handle, target, changes)

def remove_feed(target):
    handle = database.connect(config.database_file, config.sql_file)

    database.remove_feed(handle, target)

def list_episode(target):
    handle = database.connect(config.database_file, config.sql_file)

    print(json.dumps(database.search_episode(handle, target), indent = 2))

def add_episode(target):
    handle = database.connect(config.database_file, config.sql_file)

    database.add_episode(handle, target)

def modify_episode(target, changes):
    handle = database.connect(config.database_file, config.sql_file)

    database.update_episode(handle, target, changes)

def remove_episode(target):
    handle = database.connect(config.database_file, config.sql_file)

    database.remove_episode(handle, target)

def update_database():
    handle = database.connect(config.database_file, config.sql_file)

    feeds = database.search_feed(handle, {})
    for feed in feeds:
        rss = feedparser.parse(feed["link"])

        for episode in rss["entries"]:
            for link in episode["links"]:
                if link["type"].startswith("audio"):
                    database.add_episode(handle, {
                        "feed": feed["title"],
                        "title": episode["title"],
                        "date": int(dateutil.parser.parse(episode["published"]).timestamp()),
                        "link": link["href"],
                        "file": "",
                    })

def download_files():
    handle = database.connect(config.database_file, config.sql_file)
    
    feeds = database.search_feed(handle, {})
    for feed in feeds:
        os.makedirs(feed["folder"], exist_ok = True)

        downloaded = 0
        episodes = database.search_episode(handle, {"feed": feed["title"]})
        for episode in episodes:
            if os.path.isfile(episode["file"]):
                downloaded += 1

                if downloaded > feed["number"]:
                    print(f"Removing old episode: {episode['title']}")
                    os.remove(episode["file"])
                    database.update_episode(handle, {
                        "feed": feed["title"],
                        "title": episode["title"]
                    }, {
                        "file": ""
                    })
                
                else:
                    print(f"Skipped downloaded episode: {episode['title']}")

            elif downloaded < feed["number"]:
                temp = os.path.join(config.temporary_root, "downloading" + os.path.splitext(urllib.parse.urlparse(episode["link"]).path)[1])
                path = os.path.join(feed["folder"], episode["title"] + ".mp3")

                print(f"Downloading episode: {episode['title']}")
                request = requests.get(episode["link"], allow_redirects = True, stream = True, headers = { "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36" })
                request.raise_for_status()
                with open(temp, "wb") as output:
                    for chunck in request.iter_content(chunk_size = 1024 * 1024):
                        if chunck:
                            output.write(chunck)

                subprocess.run([
                    "ffmpeg", "-n", "-nostdin", "-nostats", "-loglevel", "0",
                    "-i", temp,
                    "-codec:a", "libmp3lame",
                    "-qscale:a", "6",
                    path
                ])
                os.remove(temp)

                database.update_episode(handle, {
                    "feed": feed["title"],
                    "title": episode["title"]
                }, {
                    "file": path
                })

                downloaded += 1


def download_files_multithread():
    def run(id, size, lock, shared):
        handle = database.connect(config.database_file, config.sql_file)

        while True:
            index = -1
            with lock:
                if shared["index"] < len(shared["episodes"]):
                    index = shared["index"]
                    shared["index"] += 1

                else:
                    index = -1

            if index == -1:
                break

            action = "ignore"
            with lock:
                if os.path.isfile(shared["episodes"][index]["file"]):
                    shared["downloaded"] += 1

                    if shared["downloaded"] > shared["feed"]["number"]:
                        action = "remove"

                    else:
                        action = "skip"

                elif shared["downloaded"] < shared["feed"]["number"]:
                    shared["downloaded"] += 1

                    action = "download"

            if action == "remove":
                print(f"Removing old episode: {shared['episodes'][index]['title']}")

                os.remove(shared["episodes"][index]["file"])
                database.update_episode(handle, {
                    "feed": shared["feed"]["title"],
                    "title": shared["episodes"][index]["title"]
                }, {
                    "file": ""
                })            

            elif action == "download":
                print(f"Downloading new episode: {shared['episodes'][index]['title']}")

                temp = os.path.join(config.temporary_root, "podcastd_temp_thread" + str(id) + os.path.splitext(urllib.parse.urlparse(shared["episodes"][index]["link"]).path)[1])
                path = os.path.join(shared["feed"]["folder"], shared["episodes"][index]["title"] + ".mp3")

                request = requests.get(shared["episodes"][index]["link"], allow_redirects = True, stream = True, headers = { "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36" })
                request.raise_for_status()
                with open(temp, "wb") as output:
                    for chunck in request.iter_content(chunk_size = 1024 * 1024):
                        if chunck:
                            output.write(chunck)

                subprocess.run([
                    "ffmpeg", "-n", "-nostdin", "-nostats", "-loglevel", "0",
                    "-i", temp,
                    "-codec:a", "libmp3lame",
                    "-qscale:a", "6",
                    path
                ])
                os.remove(temp)

                database.update_episode(handle, {
                    "feed": shared["feed"]["title"],
                    "title": shared["episodes"][index]["title"]
                }, {
                    "file": path
                })

            elif action == "skip":
                print(f"Skipping downloaded episode: {shared['episodes'][index]['title']}")

            # else:
            #     print(f"Ignoring episode: {shared['episodes'][index]['title']}")

    
    handle = database.connect(config.database_file, config.sql_file)
    
    feeds = database.search_feed(handle, {})
    for feed in feeds:
        os.makedirs(feed["folder"], exist_ok = True)

        lock = threading.Lock()
        threads = []
        shared = {
            "index": 0,
            "downloaded": 0,
            "feed": feed,
            "episodes": database.search_episode(handle, {"feed": feed["title"]})
        }

        for i in range(0, config.thread_count):
            threads.append(threading.Thread(target = run, args = (i, config.thread_count, lock, shared, )))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()        
        
