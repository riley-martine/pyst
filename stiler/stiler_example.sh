#!/bin/bash 

xfce4-terminal
python3 /home/riley/Projects/tools/stiler/stiler.py top_left

xfce4-terminal
python3 /home/riley/Projects/tools/stiler/stiler.py bottom_left

xfce4-terminal --working-directory=/home
python3 /home/riley/Projects/tools/stiler/stiler.py right
