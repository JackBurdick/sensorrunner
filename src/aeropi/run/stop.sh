#!/bin/bash

## stop daemon
sudo /etc/init.d/celeryd stop
echo "stopped daemon"
sudo /etc/init.d/celerybeat stop
echo "stopped beat"