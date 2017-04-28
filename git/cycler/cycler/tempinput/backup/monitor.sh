#!/bin/bash
inotifywait -m /home/jack/Desktop/temp -e create -e moved_to |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'"
        DATE=$(date +"%Y%m%d%H%M")
        mv $file $DATE.jpg
    done
