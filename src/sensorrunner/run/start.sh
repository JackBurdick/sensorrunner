#!/bin/bash
yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }

#https://stackoverflow.com/questions/59895/how-to-get-the-source-directory-of-a-bash-script-from-within-the-script-itself
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

while getopts z: option
  do
  case "${option}"
    in
      z ) CUR_CONFIG_FILE=${OPTARG};;
  esac
done

# -z option is mandatory
if [ -z ${CUR_CONFIG_FILE+x} ]; then
  die "no config file passed, please pass with \`-z path/to/spec.yml\`"
fi

## set varibables according to current spec
_file_name="daemonize_cmd.sh"
_set_daemon_vars_cmd="$DIR/$_file_name -z $CUR_CONFIG_FILE"
sudo $_set_daemon_vars_cmd

## start daemon
sudo /etc/init.d/celeryd start
echo "started daemon"
sudo /etc/init.d/celerybeat start
echo "started beat"

## start events
# TODO: only start if needed
_start_events_path="start_events.sh"
_start_events_cmd="$DIR/$_start_events_path"
echo "starting... $_start_events_cmd"
_events_pid=$($_start_events_cmd)
echo "started events, pid: $_events_pid"

$_events_pid &
echo $!
echo "done"
