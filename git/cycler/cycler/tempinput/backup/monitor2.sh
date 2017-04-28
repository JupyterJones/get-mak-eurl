#!/bin/bash
inotifywait -m /home/jack/git/clouddream/deepdream/outputs -e create -e moved_to |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'"
cp /home/jack/git/clouddream/deepdream/outputs/$file ~/Desktop/cycler/
sleep 15
cp *.jpg /home/jack/Desktop/cycler/store/perm
sleep 5
mogrify -crop 620x620+40+40 *.jpg
sleep 5
mogrify -resize 700x700 *.jpg
sleep 5
mv *.jpg /home/jack/Desktop/cycler/store/

  done
    
