#!/bin/bash
inotifywait -m /home/jack/git/clouddream/deepdream/outputs -e create -e moved_to |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'"

cp /home/jack/git/clouddream/deepdream/outputs/$file /home/jack/Desktop/cycler/store/perm/
cp /home/jack/git/clouddream/deepdream/outputs/$file /home/jack/Desktop/cycler/
echo "here1"
mogrify -crop 630x630+5+5 $file
echo "here1"
sleep 20
mogrify -resize 640x640 $file
sleep 15
echo " '$file' is ready"
mv /home/jack/Desktop/cycler/$file /home/jack/Desktop/cycler/store/
done

