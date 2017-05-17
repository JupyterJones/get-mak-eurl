#!/bin/bash
#$1 =location;\
ffmpeg = '/opt/local/bin/ffmpeg';\
image = 'testvid/image.jpg';\
interval = 5;\
size = '320x240';\
"filename" =date +%Y-%m-%d.%H:%M:%S
today=`date '+%Y_%m_%d__%H_%M_%S'`;
filename="$today.jpg"

ffmpeg -i $1 -pix_fmt yuvj422p -deinterlace -an -ss 5 -f mjpeg -t 1 -r 1 -y -s 75x75 /home/jack/Videos/vidicons/$filename 2>&1;\
echo \<a href="$1"\>\<img src=\"/home/jack/Videos/vidicons/$filename\"\>\</a\>\ >>/home/jack/Desktop/vidlist.html



