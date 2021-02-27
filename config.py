import os
import sys
import json

# these cannot be changed with the config file
user_dir = os.path.expanduser("~")
config_dir = os.path.join(user_dir, ".config", "podcastd")
config_file = os.path.join(config_dir, "config.json")
database_code = os.path.join(sys.path[0], "database.sql")

# these are configurable
default_number = 1
default_root = os.path.join(user_dir, "Downloads")
database_file = os.path.join(config_dir, "database.sqlite3")
temporary_root = os.path.join(user_dir, ".cache", "podcastd")
thread_count = os.cpu_count()

# create the config folder if doesn't exist yet
os.makedirs(config_dir, exist_ok = True)

# create a default config file if it doesn't exist yet
if not os.path.isfile(config_file):
    open(config_file, "w").write(json.dumps({
        "default_number": default_number,
        "default_root": default_root,
        "database_file": database_file,
        "temporary_root": temporary_root,
        "thread_count": thread_count
    }, indent = 2))

# load the config file
settings = json.loads(open(os.path.expanduser(config_file)).read())
    
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