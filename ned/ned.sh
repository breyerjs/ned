#!/bin/bash
while :  # while true
do
    # If there's no python scripts running, kick ned off
    # If there are, loop
    pgrep -lf python; if [ $? != 0 ]; then python ned.py; fi
done