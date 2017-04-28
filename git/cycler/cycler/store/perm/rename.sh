#!/bin/bash
inotifywait -m /home/jack/Desktop/cycler/store/perm -e create -e moved_to |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'"
       a=1
for i in *.jpg; do
  new=$(printf "%04d.jpg" "$a") #04 pad to length of 4
  mv -- "$i" "$new"
  let a=a+1
done
sleep 5
if [ $new = 0050.jpg ]
then
ffmpeg -framerate 2 -i %04d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p $new.mp4
fi
  done

  
