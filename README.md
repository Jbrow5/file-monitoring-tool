# James Brown
Real-Time File System Monitoring Tool
Created by James Brown
Copyright (C) 2024 James Brown
The Real-Time File System Monitoring Tool is a Python application designed to help security analysts and digital forensics professionals monitor and track file system activity in real time. This tool logs changes such as file creations, deletions, modifications, and movements, offering instant alerts for significant events. With its customizable settings and efficient debouncing system, this tool helps ensure accurate and manageable monitoring without overwhelming users with redundant notifications.
How to Use:
This application operates via the command line and requires Python, along with the dependencies listed in the requirements.txt file. 
Starting the tool:
python file_monitor.py help
This command displays a basic help guide outlining the tool's functionality.
python file_monitor.py <directory_path> (the path you want to monitor)
This command begins the monitoring process for the given directory. The tool will automatically track file changes and provide logs and notifications based on the detected activity.
Features Overview:
File System Activity Tracking:
•	File Events: The tool detects a range of file system activities, such as file creation, modification, deletion, and renaming or moving.
•	Event Logging: All tracked events are logged with relevant details like timestamps, file paths, and the type of action performed, ensuring a comprehensive record for further analysis.
•	Real-Time Notifications: Users are immediately notified via desktop alerts when important file events are detected, helping security professionals act quickly in response to suspicious activity.
Debouncing Alerts:
The tool includes a debouncing mechanism to avoid receiving excessive notifications for repeated actions within a short window. This ensures only a single alert is sent for similar events, reducing noise and improving the efficiency of alerts.
Event Types Monitored:
The tool logs and notifies users about the following events:
•	File Creation: Logs and alerts when new files are added to the directory.
•	File Deletion: Tracks and notifies when files are removed from the directory.
•	File Modification: Monitors file changes and sends an alert if any modification occurs.
•	File Movement/Renaming: Identifies when files or directories are moved or renamed and logs this event accordingly.
Excluding Unnecessary Files:
The tool automatically filters out temporary files (such as .tmp or .swp files), which are often irrelevant for forensics and security monitoring, ensuring that only significant changes are logged and alerted.
Code Structure:
Core Libraries Utilized:
•	os: Provides functions for handling file paths and system-level operations, such as directory management.
•	time: Used for managing event timestamps and implementing delay mechanisms for debouncing.
•	threading: Supports simultaneous monitoring and notification processes, ensuring the tool remains responsive while tracking events.
•	watchdog: A third-party library that enables real-time file system monitoring by detecting changes in the specified directory.
•	logging: Responsible for logging event details, such as file paths, changes, and timestamps, in an accessible format.
•	winotify: Allows the tool to send desktop notifications to the user when important changes are detected in the monitored directory.
Notable Functions:
•	log_event(): Logs each event into a file with detailed information (file name, event type, timestamp).
•	send_notification(): Sends a desktop alert whenever a monitored event occurs.
•	schedule_notification(): Ensures the tool doesn't block execution by processing notifications in the background.
•	debounce_notification(): Implements the debouncing feature, which prevents excessive notifications by managing cooldown periods between alerts.
•	filter_temporary_files(): Detects and ignores temporary or irrelevant files, preventing unnecessary logs or notifications.
Event Handling:
•	on_modified(): Activates when a file is altered, logs the modification, and notifies the user.
•	on_created(): Triggered when a file is created, logging the event and sending a notification.
•	on_deleted(): Detects file deletions, logs the event, and notifies the user.
•	on_moved(): Recognizes when files or directories are moved or renamed and logs the change.
•	exclude_temporary_files(): Automatically filters out files like .bak or .log to avoid unnecessary alerts.
How It Functions:
1.	Monitoring: The application begins by monitoring a specified directory for changes, such as file creations, deletions, and modifications.
2.	Event Logging: Each detected event is logged with information such as the event type, file name, and timestamp.
3.	Notifications: When significant events occur, users receive instant desktop notifications with key details about the change.
4.	Debouncing: The debouncing mechanism ensures that repeated actions don't result in multiple notifications for the same event.
Running the Tool:
To start monitoring a specific directory, run the following command:
python file_monitor.py <directory_path> (the path you want to monitor)
This will begin monitoring the specified directory for file system changes.
Conclusion:
The Real-Time File System Monitoring Tool is a practical tool for security professionals and digital forensics experts who need to monitor and respond to file system changes efficiently. By automating event logging, notifications, and ignoring unnecessary files, it simplifies the monitoring process. The user-friendly interface and customization options provide a reliable tool for monitoring file system activity and ensuring the integrity of files in sensitive environments.

