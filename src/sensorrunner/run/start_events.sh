#!/bin/bash
yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }


#https://stackoverflow.com/questions/59895/how-to-get-the-source-directory-of-a-bash-script-from-within-the-script-itself
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
_file_name="events.py"

# which python is being used
py_name="$(which python)"
_default_pi_python="/home/pi/.conda/envs/aero/bin/python"
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

_module_script="$DIR/$_file_name"

_my_cmd="$_py_cmd $_module_script &"

# stop background events
sudo ps aux|grep '/sensorrunner/src/sensorrunner/run/events.py' | awk '{print $2}' | xargs sudo kill -9

# I'm unsure why, but the script would hang if called from here
echo $_my_cmd