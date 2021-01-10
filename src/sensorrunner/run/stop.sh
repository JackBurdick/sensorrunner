#!/bin/bash

## stop daemon
sudo /etc/init.d/celeryd stop
echo "stopped daemon"
sudo /etc/init.d/celerybeat stop
echo "stopped beat"

# stop background events
sudo ps aux|grep '/sensorrunner/src/sensorrunner/run/events.py' | awk '{print $2}' | xargs sudo kill -9

# kill any remaining celery, this is fairly unsafe, but using for now
sudo ps aux|grep 'celery'| awk '{print $2}' | xargs kill -9

# TODO: generalize
/home/pi/redis-6.0.6/src/redis-cli -h localhost -p 6379 -n 1 FLUSHDB