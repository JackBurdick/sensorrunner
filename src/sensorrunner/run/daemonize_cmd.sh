#!/bin/bash

# https://stackoverflow.com/questions/1378274/in-a-bash-script-how-can-i-exit-the-entire-script-if-a-certain-condition-occurs
yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }

CELERYD_FILE_PATH="/etc/default/celeryd"
CELERYBEAT_FILE_PATH="/etc/default/celerybeat"

# If we wnated to implement logic for checking existing vars
# . "$CELERYD_FILE_PATH"
# . "$CELERYBEAT_FILE_PATH"

# `:` in `z:` indicates that a value is required
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


_python_script="daemon_args.py"

#https://stackoverflow.com/questions/59895/how-to-get-the-source-directory-of-a-bash-script-from-within-the-script-itself
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
_module_script="$DIR/$_python_script"

# which python is being used
py_name="$(which python)"
# TODO: change
#_default_pi_python="/home/pi/.conda/envs/aero/bin/python"
_default_pi_python="/home/pi/aero/bin/python"
_default_laptop_python="/home/jackburdick/anaconda3/envs/aerodev/bin/python"

# which device is currently being used
_device_pi_name="root"
_device_cur_name="$(whoami)"

# see if sensorrunner is installed
# var set?
# https://stackoverflow.com/questions/3601515/how-to-check-if-a-variable-is-set-in-bash
# but modified for this particular example
_lib_not_avail="$( python -c "import sensorrunner" 2>&1 )"
if [ "$_lib_not_avail" != "" ]; then
  # sensorrunner is not present
  # set python to the default python for the current device
  if [ $_device_cur_name == $_device_pi_name ]; then
    _py_cmd=$_default_pi_python
  else
    _py_cmd=$_default_laptop_python
  fi
else
  # sensorrunner is available in current python
  _py_cmd=$py_name 
fi


# build variables
CELERYD_NODES=""
CELERYD_WORKER_OPTS=""
CELERY_Z_OPT=""
i=0
while read line ; do
  if [ $i == 0 ]
    then
      CELERYD_NODES+=$line
  elif [ $i == 1 ]
    then
      CELERYD_WORKER_OPTS+=$line
  elif [ $i == 2 ]
    then
      CELERY_Z_OPT+=$line
  else
    die "Too many lines recieved from $_module_script"
  fi
  ((++i))
done < <($_py_cmd $_module_script $CUR_CONFIG_FILE)


## defaults
# celeryd
# TODO: change
# CELERYD_CHDIR="/home/pi/dev/sensorrunner/src/sensorrunner"
CELERYD_CHDIR="/home/pi/dev/github/sensorrunner/src/sensorrunner"
CELERY_APP="celery_app"
# TODO: change
# CELERY_BIN="/home/pi/.conda/envs/aero/bin/python -m celery"
CELERY_BIN="/home/pi/aero/bin/python -m celery"
# TODO: parameterize
CELERYD_LOG_LEVEL="INFO"

# %n will be replaced with the first part of the nodename.
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_PID_FILE="/var/run/celery/%n.pid"
CELERYD_USER="pi"
CELERYD_GROUP="pi"
CELERY_CREATE_DIRS=1
CELERY_VISIBILITY_TIMEOUT=12000

# add z opt to celeryd, default to concurrency 1
CELERYD_OPTS="--without-gossip -P solo -c 1 $CELERYD_WORKER_OPTS $CELERY_Z_OPT"

#celerybeat
#CELERYBEAT_OPTS="-Z '/home/pi/dev/sensorrunner/scratch/config_run/configs/basic_i2c.yml'"
CELERYBEAT_OPTS=$CELERY_Z_OPT

# SET DEFAULT VARIABLES
_to_remove="declare -- "
# NOTE: sed is used to remove the "declare -- " portion left over from typeset.
# I'm certain there is a better way to set the varibles, but I'm not sure how to
# do that yet, and this method does achieve the desired outcome despite being clumbsy
# set variables for celeryd
#typeset -p CELERYD_NODES CELERYD_OPTS> "$CELERYD_FILE_PATH"
typeset -p CELERYD_CHDIR CELERYD_NODES CELERY_APP CELERY_BIN CELERYD_OPTS \
  CELERYD_LOG_LEVEL CELERYD_LOG_FILE CELERYD_PID_FILE CELERYD_USER CELERYD_GROUP CELERY_CREATE_DIRS CELERY_VISIBILITY_TIMEOUT > "$CELERYD_FILE_PATH"
sudo sed -i "s/${_to_remove}//g" ${CELERYD_FILE_PATH}
# set variables for celerybeat

typeset -p CELERYBEAT_OPTS> "$CELERYBEAT_FILE_PATH"
sudo sed -i "s/${_to_remove}//g" ${CELERYBEAT_FILE_PATH}
