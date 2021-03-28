#!/bin/sh
# launcher.sh
# navigate to home directory, then this directory, then execute python script, then back home

sleep 5

cd /
# sudo mount /dev/sda /media/pi/AUDIO
cd /home/pi/Documents/clawMachine/src
sudo python3 run_time.py
cd /
