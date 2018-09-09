#!/bin/bash

# This is a wrapper for the ned.py script
# If it crashes, this will try to kick it off again.

while :  # while true
do
    # If there's no python scripts running, kick ned off
    # If there are, loop
    pgrep -lf python; if [ $? != 0 ]; then python3 ned.py; fi
done
