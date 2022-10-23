import pyinotify
import os

databaseinfo = os.getenv('dbinfo')
pathtowatch = os.getenv('watchpath')


wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events

import sqlite3
connection = sqlite3.connect(databaseinfo, timeout=20)
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id TEXT, filename TEXT, rdstatus TEXT, rdprogressdownload INTEGER, attemptstogetlink INTEGER, rderror TEXT , completed TEXT , Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP )")


class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        head, tail = os.path.split(event.pathname)
        filename = (tail)
        extension = os.path.splitext(filename)[1][1:]

        match extension:
            case "torrent":
                print("Torrent file detected ",tail)
                torrent=(event.pathname)
                import subprocess
                process = subprocess.Popen(['python', 'RDtorrent.py', torrent])

            case "magnet":
                print("Magnet file detected ",tail)
                magnetlink = (event.pathname)
                import subprocess
                process = subprocess.Popen(['python', 'RDmagnet.py', magnetlink])

            case _:
                print("IGNORE Not suitable - " , tail)




handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(pathtowatch, mask, rec=True)
notifier.loop()

