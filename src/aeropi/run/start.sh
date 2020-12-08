#!/bin/bash
yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }

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


_user="jackburdick"

## set varibables according to current spec
_file_name="daemonize_cmd.sh"
cmd="$PWD/$_file_name -z $CUR_CONFIG_FILE"
sudo -u $_user $cmd

## start daemon
sudo /etc/init.d/celeryd start
echo "started daemon"
sudo /etc/init.d/celerybeat start
echo "started beat"