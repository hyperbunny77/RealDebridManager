# Real Debrid Manager

Docker Repo : [https://hub.docker.com/r/hyperbunny77/realdebridmanager](https://hub.docker.com/r/hyperbunny77/realdebridmanager)

This project aims to automate many functions of the Real Debrid Service.
It is intended to slot into your existing workflows. Please see examples below.

### __**Core Functionality :**__

* Detect torrent file in watched folder.
* Submit to Real Debrid for action.
* Watch/manage Real Debrid until file is ready for download.
* Get Real Debrid link to files in torrent.
* Send to local download client (Aria2).

## Core Setup :

Deploy the application via the use of docker. Please use the below docker compose as a template :

```
  realdebridmanager:
    image: hyperbunny77/realdebridmanager:2022.05.22   #Change to your chosen release
    container_name: realdebridmanager
    environment:
      - PUID=0
      - PGID=0
    ports:
      - 5000:5000/tcp 	
    volumes:
      - torrent_folder_to_watch:/watch
      - path_for_config_storage:/config
    restart: unless-stopped
```

## Examples :

### Sonarr/Radarr Integration :

This application fits great into your workflow with Sonarr/Radarr.
The use of Real Debrid Manager will mean sonarr/radarr can utilise Real Debrid
as a source for downloading new files. This allows you to benefit from the many
advantages that the Real Debrid service provides.

#### Setup :



