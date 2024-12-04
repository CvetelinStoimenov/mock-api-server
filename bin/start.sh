#!/bin/bash

python3 -m gunicorn -c gunicorn.http.conf.py mock:mock &
PID1=$!
python3 -m gunicorn -c gunicorn.https.conf.py mock:mock &
PID2=$!

# Wait for both processes to complete
wait $PID1 $PID2
