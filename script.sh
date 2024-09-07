#!/bin/bash

export DISPLAY=:0

nohup python3 /home/HoloOS/GUI_TK/Server/server.py  &
nohup python3 /home/HoloOS/GUI_TK/servo-code/open_display.py  &

#startx &> /home/HoloOS7GUI_TK/output.txt
startx &> /home/HoloOS/GUI_TK/output.txt
#sleep 5
