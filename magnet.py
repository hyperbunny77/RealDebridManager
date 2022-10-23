import requests
import time
import os
import aria2p
import sqlite3

databaseinfo = os.getenv("dbinfo")
connection = sqlite3.connect(databaseinfo, timeout=20)
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS tasks (id TEXT, filename TEXT, rdstatus TEXT, rdprogressdownload INTEGER, attemptstogetlink INTEGER, rderror TEXT , completed TEXT , Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP )"
)

cursor.execute("SELECT * FROM settings where id=1")
result = cursor.fetchall()
waitbetween = result[0][1]
maxattempts = result[0][2]
aria2host = result[0][3]
secretkey = result[0][4]
rdapikey = result[0][5]


def moveprocessed(pathname, error):
    pathname = originalmagnet
    head, tail = os.path.split(pathname)
    if error == 0:
        newlocaton = head + "/processed/" + tail
        os.rename(pathname, newlocaton)
    else:
        newlocaton = head + "/errored/" + tail + ".MAGNET"
        os.rename(pathname, newlocaton)


def realdebridtorrent(magnet):
    global completed
    addmagneturl = (
        "https://api.real-debrid.com/rest/1.0/torrents/addMagnet?auth_token=" + rdapikey
    )
    magnetaddjson = {"magnet": magnet}
    response = requests.post(addmagneturl, data=magnetaddjson)
    responsefromrd = response.json()
    myid = responsefromrd["id"]
    head, tail = os.path.split(magnet)
    filename = tail
    rdstatus = "Submitted to RD"
    attemptstogetlink = 0
    rderror = " "
    completedtask = "No"
    cursor.execute(
        """INSERT INTO tasks(id, filename, rdstatus, attemptstogetlink, rderror,completed) VALUES (?,?,?,?,?,?)""",
        (myid, filename, rdstatus, attemptstogetlink, rderror, completedtask),
    )
    connection.commit()
    time.sleep(2)
    selectfiles = (
        "https://api.real-debrid.com/rest/1.0/torrents/selectFiles/"
        + myid
        + "?auth_token="
        + rdapikey
    )
    allfiles = {"files": "all"}
    response = requests.post(selectfiles, data=allfiles)

    selecttorrentinfo = (
        "https://api.real-debrid.com/rest/1.0/torrents/info/"
        + myid
        + "?auth_token="
        + rdapikey
    )
    response = requests.get(selecttorrentinfo)
    responsefromrd = response.json()
    status = responsefromrd["status"]

    match status:
        case "downloaded":
            completed = 1
        case "queued":
            completed = 0
        case "magnet_error":
            rdstatus = "Magnet Error"
            cursor.execute(
                """INSERT INTO tasks(id, filename, rdstatus, rdprogressdownload, attemptstogetlink, rderror,completed) VALUES (?,?,?,?,?,?,?)""",
                (
                    myid,
                    filename,
                    rdstatus,
                    rdprogressdownload,
                    attemptstogetlink,
                    rderror,
                    completedtask,
                ),
            )
            connection.commit()
            completed = 1
            global error
            error = 1
            moveprocessed(magnet, error)
        case "error":
            rdstatus = "General Error"
            cursor.execute(
                """INSERT INTO tasks(id, filename, rdstatus, rdprogressdownload, attemptstogetlink, rderror,completed) VALUES (?,?,?,?,?,?,?)""",
                (
                    myid,
                    filename,
                    rdstatus,
                    rdprogressdownload,
                    attemptstogetlink,
                    rderror,
                    completedtask,
                ),
            )
            connection.commit()
            completed = 1
            error = 1
            moveprocessed(magnet, error)
        case "magnet_conversion":
            rdstatus = "Stuck Magnet Conversion"
            cursor.execute(
                """INSERT INTO tasks(id, filename, rdstatus, rdprogressdownload, attemptstogetlink, rderror,completed) VALUES (?,?,?,?,?,?,?)""",
                (
                    myid,
                    filename,
                    rdstatus,
                    rdprogressdownload,
                    attemptstogetlink,
                    rderror,
                    completedtask,
                ),
            )
            connection.commit()
            completed = 1
            error = 1
            moveprocessed(magnet, error)
        case "virus":
            rdstatus = "File is Virus"
            cursor.execute(
                """INSERT INTO tasks(id, filename, rdstatus, rdprogressdownload, attemptstogetlink, rderror,completed) VALUES (?,?,?,?,?,?,?)""",
                (
                    myid,
                    filename,
                    rdstatus,
                    rdprogressdownload,
                    attemptstogetlink,
                    rderror,
                    completedtask,
                ),
            )
            connection.commit()
            completed = 1
            error = 1
            moveprocessed(magnet, error)
        case "dead":
            rdstatus = "Link is Dead"
            cursor.execute(
                """INSERT INTO tasks(id, filename, rdstatus, rdprogressdownload, attemptstogetlink, rderror,completed) VALUES (?,?,?,?,?,?,?)""",
                (
                    myid,
                    filename,
                    rdstatus,
                    rdprogressdownload,
                    attemptstogetlink,
                    rderror,
                    completedtask,
                ),
            )
            connection.commit()
            completed = 1
            error = 1
            moveprocessed(magnet, error)
        case _:
            completed = 0

    while completed == 0:
        selecttorrentinfo = (
            "https://api.real-debrid.com/rest/1.0/torrents/info/"
            + myid
            + "?auth_token="
            + rdapikey
        )
        response = requests.get(selecttorrentinfo)
        responsefromrd = response.json()
        if responsefromrd["status"] == "downloaded":
            completed = 1
        else:
            completed = 0
        rdstatus = "Downloading"
        attemptstogetlink = attemptstogetlink + 1
        rdprogressdownload = responsefromrd["progress"]
        completedtask = "No"
        rderror = "No error"
        cursor.execute(
            """INSERT INTO tasks(id, filename, rdstatus, rdprogressdownload, attemptstogetlink, rderror,completed) VALUES (?,?,?,?,?,?,?)""",
            (
                myid,
                filename,
                rdstatus,
                rdprogressdownload,
                attemptstogetlink,
                rderror,
                completedtask,
            ),
        )
        connection.commit()
        if attemptstogetlink >= maxattempts:
            completed = 2
        else:
            time.sleep(waitbetween)

    if completed == 1:
        rdstatus = "Downloaded to RD"
        attemptstogetlink = attemptstogetlink
        rderror = "none"
        completedtask = "Yes"
        rdprogressdownload = 100
        cursor.execute(
            """INSERT INTO tasks(id, filename, rdstatus, attemptstogetlink, rderror,rdprogressdownload,completed) VALUES (?,?,?,?,?,?,?)""",
            (
                myid,
                filename,
                rdstatus,
                attemptstogetlink,
                rderror,
                rdprogressdownload,
                completedtask,
            ),
        )
        connection.commit()
        aria2 = aria2p.API(aria2p.Client(host=aria2host, port=6800, secret=secretkey))
        error = 0
        links = responsefromrd["links"]
        for i in range(len(links)):
            getdownloadlinkurl = (
                "https://api.real-debrid.com/rest/1.0/unrestrict/link?auth_token="
                + rdapikey
            )
            filetoselect = {"link": links[i]}
            response = requests.post(getdownloadlinkurl, data=filetoselect)
            responsefromrd = response.json()
            mylink = responsefromrd["download"]
            try:
                download = aria2.add(mylink)
            except:
                print("Error Connecting To Your ARIA2 Instance")
        moveprocessed(magnet, error)
        time.sleep(1)
        rdstatus = "Sent to aria2"
        cursor.execute(
            """INSERT INTO tasks(id, filename, rdstatus, attemptstogetlink, rderror,rdprogressdownload,completed) VALUES (?,?,?,?,?,?,?)""",
            (
                myid,
                filename,
                rdstatus,
                attemptstogetlink,
                rderror,
                rdprogressdownload,
                completedtask,
            ),
        )
        connection.commit()

    elif completed == 2:
        time.sleep(1)
        deletetorrentfromrd = (
            "https://api.real-debrid.com/rest/1.0/torrents/delete/"
            + myid
            + "?auth_token="
            + rdapikey
        )
        response = requests.delete(deletetorrentfromrd)
        error = 1
        rdstatus = "Max Timeout Reached"
        attemptstogetlink = attemptstogetlink
        rderror = "Max Time"
        completedtask = "No"
        cursor.execute(
            """INSERT INTO tasks(id, filename, rdstatus, attemptstogetlink, rderror,rdprogressdownload,completed) VALUES (?,?,?,?,?,?,?)""",
            (
                myid,
                filename,
                rdstatus,
                attemptstogetlink,
                rderror,
                rdprogressdownload,
                completedtask,
            ),
        )
        connection.commit()
        moveprocessed(magnet, error)


import sys

originalmagnet = sys.argv[1]
print("Starting Script on Received Magnet")
with open(originalmagnet, "r") as f:
    magnetlink = f.readlines()
magnetlink = magnetlink[0]
realdebridtorrent(magnetlink)
