import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

LOG_FILE = "/home/ubuntu/bsm/logs/changes.json"
WATCH_DIRECTORY = "/home/ubuntu/bsm/test"

class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        change = {
            "event_type": event.event_type,
            "src_path": event.src_path,
            "is_directory": event.is_directory,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Log the change to a JSON file
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w') as f:
                json.dump([], f)

        with open(LOG_FILE, 'r+') as f:
            data = json.load(f)
            data.append(change)
            f.seek(0)
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=True)

    print(f"Watching for changes in: {WATCH_DIRECTORY}")
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
