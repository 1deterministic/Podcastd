import os
import sys
import requests
import threading

import defaults
import database
import actions

# python3 -B podcastd.py --list
# python3 -B podcastd.py --update [--title title]*
# python3 -B podcastd.py --add --link https://url [--title title] [--number N] [--folder /path/to/folder]
# python3 -B podcastd.py --modify --title title [--new-title new-title] [--new-link https://new-url] [--new-number nN] [--new-folder /new/path/to/folder]
# python3 -B podcastd.py --remove --title title

if __name__ == "__main__":
    db = database.connect(defaults.DATABASE, defaults.SQLCODE)
    if db is None:
        print("Error connecting to the database file!")
        sys.exit(1)

    operations = []

    i = 0
    while i < len(sys.argv):
        # new operations
        if sys.argv[i] == "--list":
            operations.append({"action": "list", "target": {}, "changes": {}})

        elif sys.argv[i] == "--update":
            operations.append({"action": "update", "target": {}, "changes": {}})

        elif sys.argv[i] == "--add":
            operations.append({"action": "add", "target": {}, "changes": {}})

        elif sys.argv[i] == "--modify":
            operations.append({"action": "modify", "target": {}, "changes": {}})

        elif sys.argv[i] == "--remove":
            operations.append({"action": "remove", "target": {}, "changes": {}})

        elif sys.argv[i] == "--download":
            operations.append({"action": "download", "target": {}, "changes": {}})

        # target properties
        elif sys.argv[i] == "--title":
            if i + 1 < len(sys.argv):
                operations[-1]["target"]["title"] = sys.argv[i + 1]
            else:
                print("No title specified!")
                sys.exit(1)  
            i += 1

        elif sys.argv[i] == "--link":
            if i + 1 < len(sys.argv):
                operations[-1]["target"]["link"] = sys.argv[i + 1]
            else:
                print("No link specified!")
                sys.exit(1)
            i += 1

        elif sys.argv[i] == "--number":
            if i + 1 < len(sys.argv):
                operations[-1]["target"]["number"] = sys.argv[i + 1]
            else:
                print("No number specified!")
                sys.exit(1)
            i += 1

        elif sys.argv[i] == "--folder":
            if i + 1 < len(sys.argv):
                operations[-1]["target"]["folder"] = sys.argv[i + 1]
            else:
                print("No folder specified!")
                sys.exit(1)
            i += 1

        # changes to target
        elif sys.argv[i] == "--new-title":
            if i + 1 < len(sys.argv):
                operations[-1]["changes"]["title"] = sys.argv[i + 1]
            else:
                print("No title specified!")
                sys.exit(1)
            i += 1

        elif sys.argv[i] == "--new-link":
            if i + 1 < len(sys.argv):
                operations[-1]["changes"]["link"] = sys.argv[i + 1]
            else:
                print("No link specified!")
                sys.exit(1)
            i += 1

        elif sys.argv[i] == "--new-number":
            if i + 1 < len(sys.argv):
                operations[-1]["changes"]["number"] = sys.argv[i + 1]
            else:
                print("No number specified!")
                sys.exit(1)
            i += 1

        elif sys.argv[i] == "--new-folder":
            if i + 1 < len(sys.argv):
                operations[-1]["changes"]["folder"] = sys.argv[i + 1]
            else:
                print("No folder specified!")
                sys.exit(1)
            i += 1

        i += 1


    for operation in operations:
        # print(operation["action"], operation["target"], operation["changes"])

        if operation["action"] == "list":
            actions.doList(db, operation["target"])

        elif operation["action"] == "update":
            actions.doUpdate(db, operation["target"])

        elif operation["action"] == "add":
            actions.doAdd(db, operation["target"])

        elif operation["action"] == "modify":
            actions.doModify(db, operation["target"], operation["changes"])

        elif operation["action"] == "remove":
            actions.doRemove(db, operation["target"])

        elif operation["action"] == "download":
            actions.doDownload(db, operation["target"])