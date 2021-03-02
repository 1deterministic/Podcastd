import os
import sys
import json
import subprocess

user_dir = subprocess.check_output("xdg-user-dir HOME", shell = True, env = os.environ).decode("utf-8").replace("\n", "")
config_dir = os.path.join(user_dir, ".config", "podcastd")
cache_dir = os.path.join(user_dir, ".cache", "podcastd")

# these cannot be changed with the config file
config_file = os.path.join(config_dir, "config.json")
database_code = os.path.join(sys.path[0], "database.sql")

# these are configurable
default_number = 1
default_root = subprocess.check_output("xdg-user-dir DOWNLOAD", shell = True, env = os.environ).decode("utf-8").replace("\n", "")
database_file = os.path.join(config_dir, "database.sqlite3")
temporary_root = cache_dir
thread_count = os.cpu_count()
copy_command = "cp \"$downloaded_file\" ::\"$feed_folder\"/\"$episode_title\".\"${downloaded_file##*.}\"::" # put the output file string between '::' so that it can save the path in the database (not particularly proud of this)
# copy_command = "ffmpeg -n -nostdin -nostats -loglevel 0 -i \"$downloaded_file\" -codec:a libmp3lame -qscale:a 6 ::\"$feed_folder\"/\"$episode_title\".\"${downloaded_file##*.}\"::" # something like this will convert the downloaded file with ffmpeg

# create the config folder if doesn't exist yet
os.makedirs(config_dir, exist_ok = True)

# create a default config file if it doesn't exist yet
if not os.path.isfile(config_file):
    open(config_file, "w").write(json.dumps({
        "default_number": default_number,
        "default_root": default_root,
        "database_file": database_file,
        "temporary_root": temporary_root,
        "thread_count": thread_count,
        "copy_command": copy_command
    }, indent = 2))

# load the config file
settings = json.loads(open(config_file).read())
    
if "default_number" in settings.keys():
    default_number = settings["default_number"]

if "default_root" in settings.keys():
    default_root = settings["default_root"]

if "database_file" in settings.keys():
    database_file = settings["database_file"]

if "temporary_root" in settings.keys():
    temporary_root = settings["temporary_root"]

if "thread_count" in settings.keys():
    thread_count = settings["thread_count"]

if "copy_command" in settings.keys():
    copy_command = settings["copy_command"]

# debug
# print("user_dir:", user_dir)
# print("config_dir:", config_dir)
# print("config_file:", config_file)
# print("database_code:", database_code)
# print("default_number:", default_number)
# print("default_root:", default_root)
# print("database_file:", database_file)
# print("temporary_root:", temporary_root)
# print("thread_count:", thread_count)
# print("copy_output:", copy_output)