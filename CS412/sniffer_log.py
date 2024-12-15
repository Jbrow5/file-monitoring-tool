# Author: James Brown
#CS412 12/13/2024

import os
import time
import threading
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from winotify import Notification

# Set up logging for activity in the monitored folder/files
LOG_FILE_PATH = "C:/Users/samoj/OneDrive/Documents/CS412/system_monitor_log.txt"
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Add the timestamp to the logged activity
last_event = {"timestamp": time.time(), "event": ""}

# Function to log events into a file
def log_event(event_message):
    logging.info(event_message)

# Function to send notifications using winotify
def send_notification(title, message):
    try:
        toast = Notification(app_id="System Monitor", title=title, msg=message)
        toast.show()
    except Exception as e:
        log_event(f"Notification error: {str(e)}")

# Function to schedule notification in the main thread
def schedule_notification(title, message):
    if threading.current_thread() is threading.main_thread():
        send_notification(title, message)
    else:
        threading.Thread(target=send_notification, args=(title, message)).start()

# Function to debounce notifications
def debounce_notification(title, message, cooldown=10):
    current_time = time.time()
    global last_event
    if last_event["event"] != message or current_time - last_event["timestamp"] > cooldown:
        last_event = {"timestamp": current_time, "event": message}
        schedule_notification(title, message)

# Custom event handler for detecting file system changes
class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # this will ignore modifications to the log file itself and system/temp files
        if event.src_path.endswith("system_monitor_log.txt") or self.is_temporary_file(event.src_path):
            return
        if not event.is_directory:
            log_event(f"File modified: {event.src_path}")
            debounce_notification("File Modified", f"A file was modified: {event.src_path}")

    def on_created(self, event):
        # Ignore system/temp files
        if self.is_temporary_file(event.src_path):
            return
        if event.is_directory:
            log_event(f"Folder created: {event.src_path}")
            debounce_notification("Folder Created", f"A folder was created: {event.src_path}")
        else:
            log_event(f"File created: {event.src_path}")
            debounce_notification("File Created", f"A file was created: {event.src_path}")

    def on_deleted(self, event):
        # Ignore system/temp files
        if self.is_temporary_file(event.src_path):
            return
        if event.is_directory:
            log_event(f"Folder deleted: {event.src_path}")
            debounce_notification("Folder Deleted", f"A folder was deleted: {event.src_path}")
        else:
            log_event(f"File deleted: {event.src_path}")
            debounce_notification("File Deleted", f"A file was deleted: {event.src_path}")

    def on_moved(self, event):
        # Ignore system/temp files
        if self.is_temporary_file(event.src_path) or self.is_temporary_file(event.dest_path):
            return

        src_dir = os.path.dirname(event.src_path)
        dest_dir = os.path.dirname(event.dest_path)

        # Check if the move is a rename within the same directory
        if src_dir == dest_dir:
            log_event(f"File or folder renamed: from {event.src_path} to {event.dest_path}")
            debounce_notification(
                "File/Folder Renamed", f"File or folder renamed: from {event.src_path} to {event.dest_path}"
            )
        else:
            log_event(f"File or folder moved: from {event.src_path} to {event.dest_path}")
            debounce_notification(
                "File/Folder Moved", f"File or folder moved: from {event.src_path} to {event.dest_path}"
            )

    def is_temporary_file(self, path):
        """
        Helper function to identify temporary/system files.
        Modify the patterns to suit your environment.
        """
        temp_patterns = [".part", ".crdownload", ".DS_Store", "~$", ".tmp", "desktop.ini"]
        for pattern in temp_patterns:
            if pattern in os.path.basename(path):
                log_event(f"[TEMP] File detected: {path}")
                # Return False to include temporary files in monitoring
                return True

        return False  # Monitor all files, including temporary ones

# Main function to start the monitoring
def main():
    path_to_monitor = "C:/Users/samoj/OneDrive/Documents/412"  # Path to monitor
    print(f"Monitoring path: {path_to_monitor}") #what shows in the termainl when you start the program

    # Start watchdog observer
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_monitor, recursive=True)  # Monitor subfolders as well

    try:
        observer.start()
        print("Monitoring started. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        print("Stopping monitor program...")
        observer.stop()
    observer.join()

# Run the main function
if __name__ == "__main__":
    main()
