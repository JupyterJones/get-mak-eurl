#!/bin/bash

mogrify -crop 620x620+40+40 input.jpg
sleep 5
mogrify -resize 700x700 input.jpg
exit
