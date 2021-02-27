# requires feedparser, dateutils, urllib3, requests
import sys

import actions

if __name__ == "__main__":
    operations = []
    parameter_for = None
    value_for = None

    for argument in sys.argv:
        # operation starters
        if argument == "--list-feed":
            operations.append({})
            operations[-1]["action"] = "list-feed"
            
        elif argument == "--add-feed":
            operations.append({})
            operations[-1]["action"] = "add-feed"
            
        elif argument == "--modify-feed":
            operations.append({})
            operations[-1]["action"] = "modify-feed"
            
        elif argument == "--remove-feed":
            operations.append({})
            operations[-1]["action"] = "remove-feed"

        elif argument == "--list-episode":
            operations.append({})
            operations[-1]["action"] = "list-episode"
            
        elif argument == "--add-episode":
            operations.append({})
            operations[-1]["action"] = "add-episode"
            
        elif argument == "--modify-episode":
            operations.append({})
            operations[-1]["action"] = "modify-episode"
            
        elif argument == "--remove-episode":
            operations.append({})
            operations[-1]["action"] = "remove-episode"

        elif argument == "--update-database":
            operations.append({})
            operations[-1]["action"] = "update-database"

        elif argument == "--download-files":
            operations.append({})
            operations[-1]["action"] = "download-files"
            
        # operation parameter selectors
        elif argument == "--target":
            operations[-1]["target"] = {}
            parameter_for = "target"
            
        elif argument == "--changes":
            operations[-1]["changes"] = {}
            parameter_for = "changes"
            
        # operation value selectors
        elif argument == "--title":
            value_for = "title"

        elif argument == "--link":
            value_for = "link"

        elif argument == "--number":
            value_for = "number"

        elif argument == "--folder":
            value_for = "folder"

        elif argument == "--feed":
            value_for = "feed"

        elif argument == "--date":
            value_for = "date"

        elif argument == "--link":
            value_for = "link"

        elif argument == "--file":
            value_for = "file"

        # actual value
        else:
            if len(operations) > 0 and not parameter_for == None and not value_for == None:
                operations[-1][parameter_for][value_for] = argument
    
    for operation in operations:
        # print(operation)

        if operation["action"] == "list-feed":
            if actions.list_feed(operation["target"] if "target" in operation.keys() else {}):
                print("Success!")

            else:
                print("Error!")

        elif operation["action"] == "add-feed":
            if actions.add_feed(operation["target"] if "target" in operation.keys() else {}):
                print("Success!")
                
            else:
                print("Error!")

        elif operation["action"] == "modify-feed":
            if actions.modify_feed(operation["target"] if "target" in operation.keys() else {}, operation["changes"] if "changes" in operation.keys() else {}):
                print("Success!")
                
            else:
                print("Error!")
        
        elif operation["action"] == "remove-feed":
            if actions.remove_feed(operation["target"] if "target" in operation.keys() else {})        :
                print("Success!")
                
            else:
                print("Error!")

        elif operation["action"] == "list-episode":
            if actions.list_episode(operation["target"] if "target" in operation.keys() else {}):
                print("Success!")
                
            else:
                print("Error!")

        elif operation["action"] == "add-episode":
            if actions.add_episode(operation["target"] if "target" in operation.keys() else {}):
                print("Success!")
                
            else:
                print("Error!")

        elif operation["action"] == "modify-episode":
            if actions.modify_episode(operation["target"] if "target" in operation.keys() else {}, operation["changes"] if "changes" in operation.keys() else {}):
                print("Success!")
                
            else:
                print("Error!")
        
        elif operation["action"] == "remove-episode":
            if actions.remove_episode(operation["target"] if "target" in operation.keys() else {}):
                print("Success!")
                
            else:
                print("Error!")

        elif operation["action"] == "update-database":
            if actions.update_database():
                print("Success!")
                
            else:
                print("Error!")

        elif operation["action"] == "download-files":
            if actions.download_files_multithread():
            # if actions.download_files():
                print("Success!")
                
            else:
                print("Error!")