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
    print(json.dumps(database.search_feed(target), indent = 2))

    return True


def add_feed(target):
    # use defaults if not specified
    if not "number" in target.keys():
        target["number"] = config.default_number

    if not "folder" in target.keys():
        target["folder"] = os.path.join(config.default_root, target["title"])

    return database.add_feed(target)


def modify_feed(target, changes):
    return database.update_feed(target, changes)


def remove_feed(target):
    return database.remove_feed(target)


def list_episode(target):
    print(json.dumps(database.search_episode(target), indent = 2))

    return True


def add_episode(target):
    return database.add_episode(target)


def modify_episode(target, changes):
    return database.update_episode(target, changes)


def remove_episode(target):
    return database.remove_episode(target)


def update_database():
    feeds = database.search_feed({})
    for feed in feeds:
        rss = feedparser.parse(feed["link"])

        for episode in rss["entries"]:
            for link in episode["links"]:
                if link["type"].startswith("audio"):
                    if not database.add_episode({
                        "feed": feed["title"],
                        "title": episode["title"],
                        "date": int(dateutil.parser.parse(episode["published"]).timestamp()),
                        "link": link["href"],
                        "file": "",
                    }):
                        return False

    return True


def download_files():
    feeds = database.search_feed({})
    for feed in feeds:
        try:
            os.makedirs(feed["folder"], exist_ok = True)

        except:
            return False

        downloaded = 0
        episodes = database.search_episode({"feed": feed["title"]})
        for episode in episodes:
            action = "ignore"
            if os.path.isfile(episode["file"]):
                downloaded += 1

                if downloaded > feed["number"]:
                    action = "remove"

                else:
                    action = "skip"

            elif downloaded < feed["number"]:
                downloaded += 1
                action = "download"

            if action == "remove":
                print(f"Removing old episode: {episode['title']}")

                try:
                    os.remove(episode["file"])

                except:
                    print(f"Error: Could not remove file: {episode['file']}")
                    continue

                if not database.update_episode({
                    "feed": feed["title"],
                    "title": episode["title"]
                }, {
                    "file": ""
                }):
                    print(f"Error: Could not update database to remove file reference: {episode['file']}")
                    continue

            elif action == "download":
                print(f"Downloading new episode: {episode['title']}")

                os.makedirs(config.temporary_root, exist_ok = True)

                temp = os.path.join(config.temporary_root, "podcastd_temp" + os.path.splitext(urllib.parse.urlparse(episode["link"]).path)[1])
                path = os.path.join(feed["folder"], episode["title"] + ".mp3")

                try:
                    request = requests.get(episode["link"], timeout = 10, allow_redirects = True, stream = True, headers = { "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36" })
                    # request.raise_for_status()
                    with open(temp, "wb") as output:
                        for chunck in request.iter_content(chunk_size = 1024 * 1024):
                            if chunck:
                                output.write(chunck)

                except:
                    print(f"Error: Could not download file from: {episode['link']}")
                    continue


                subprocess.run([
                    "ffmpeg", "-n", "-nostdin", "-nostats", "-loglevel", "0",
                    "-i", temp,
                    "-codec:a", "libmp3lame",
                    "-qscale:a", "6",
                    path
                ])

                try:
                    os.remove(temp)
                
                except:
                    print(f"Error: Could not remove temporary file: {temp}")
                    continue

                if not database.update_episode({
                    "feed": feed["title"],
                    "title": episode["title"]
                }, {
                    "file": path
                }):
                    print(f"Error: Could not update database to include file reference: {episode['file']}")
                    continue

            elif action == "skip":
                print(f"Skipping downloaded episode: {episode['title']}")

            # else:
            #     print(f"Ignoring episode: {episode['title']}")

    return True


def download_files_multithread():
    def run(id, size, lock, shared):
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

                try:
                    os.remove(shared["episodes"][index]["file"])

                except:
                    print(f"Error: Could not remove file: {shared['episodes'][index]['file']}")
                    continue

                if not database.update_episode({
                    "feed": shared["feed"]["title"],
                    "title": shared["episodes"][index]["title"]
                }, {
                    "file": ""
                }):
                    print(f"Error: Could not update database to remove file reference: {shared['episodes'][index]['file']}")
                    continue

            elif action == "download":
                print(f"Downloading new episode: {shared['episodes'][index]['title']}")

                os.makedirs(config.temporary_root, exist_ok = True)
                
                temp = os.path.join(config.temporary_root, "podcastd_temp_thread" + str(id) + os.path.splitext(urllib.parse.urlparse(shared["episodes"][index]["link"]).path)[1])
                path = os.path.join(shared["feed"]["folder"], shared["episodes"][index]["title"] + ".mp3")

                try:
                    request = requests.get(shared["episodes"][index]["link"], timeout = 10, allow_redirects = True, stream = True, headers = { "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36" })
                    # request.raise_for_status()
                    with open(temp, "wb") as output:
                        for chunck in request.iter_content(chunk_size = 1024 * 1024):
                            if chunck:
                                output.write(chunck)

                except:
                    print(f"Error: Could not download file from: {shared['episodes'][index]['link']}")
                    continue

                subprocess.run([
                    "ffmpeg", "-n", "-nostdin", "-nostats", "-loglevel", "0",
                    "-i", temp,
                    "-codec:a", "libmp3lame",
                    "-qscale:a", "6",
                    path
                ])

                try:
                    os.remove(temp)

                except:
                    print(f"Error: Could not remove temporary file: {temp}")
                    continue

                if not database.update_episode({
                    "feed": shared["feed"]["title"],
                    "title": shared["episodes"][index]["title"]
                }, {
                    "file": path
                }):
                    print(f"Error: Could not update database to include file reference: {shared['episodes'][index]['file']}")
                    continue

            elif action == "skip":
                print(f"Skipping downloaded episode: {shared['episodes'][index]['title']}")

            # else:
            #     print(f"Ignoring episode: {shared['episodes'][index]['title']}")

    
    feeds = database.search_feed({})
    for feed in feeds:
        try:
            os.makedirs(feed["folder"], exist_ok = True)

        except:
            return False

        lock = threading.Lock()
        threads = []
        shared = {
            "index": 0,
            "downloaded": 0,
            "feed": feed,
            "episodes": database.search_episode({"feed": feed["title"]})
        }

        for i in range(0, config.thread_count):
            threads.append(threading.Thread(target = run, args = (i, config.thread_count, lock, shared, )))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        return True