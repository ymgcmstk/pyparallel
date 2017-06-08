#!/bin/bash

ANOTHERHOST=localhost # should be changed to another machine's host name, although localhost also works

echo "parallel_toolbox.prange demo:"
ssh $ANOTHERHOST python `pwd`/example_prange.py &
python `pwd`/example_prange.py

sleep 2

echo "parallel_toolbox.plist demo (verbose mode):"
ssh $ANOTHERHOST python `pwd`/example_plist.py &
python `pwd`/example_plist.py
