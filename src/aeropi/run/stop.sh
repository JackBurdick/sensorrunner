#!/bin/bash

## stop daemon
sudo /etc/init.d/celeryd stop
echo "stopped daemon"
sudo /etc/init.d/celerybeat stop
echo "stopped beat"

# stop background events
sudo ps aux|grep '/aeropi/src/aeropi/run/events.py' | awk '{print $2}' | xargs sudo kill -9

# kill any remaining celery, this is fairly unsafe, but using for now
sudo ps aux|grep 'celery'| awk '{print $2}' | xargs kill -9