#!/bin/bash
inotifywait -m /home/jack/Desktop/cycler/store/ -e create -e moved_to |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'"
        DATE=$(date +"%Y-%m-%d-%H:%M:%S")
        mv $file $DATE.jpg
mv *.jpg /home/jack/git/clouddream/deepdream/inputs/
    done
