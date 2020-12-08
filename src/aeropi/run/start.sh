#!/bin/bash

_user="jackburdick"

## set varibables according to current spec
_file_name="daemonize_cmd.sh"
cmd="$PWD/$_file_name"
sudo -u $_user $cmd

## start daemon
sudo /etc/init.d/celeryd start
echo "started daemon"
sudo /etc/init.d/celerybeat start
echo "started beat"
