#!/bin/bash

# https://stackoverflow.com/questions/1378274/in-a-bash-script-how-can-i-exit-the-entire-script-if-a-certain-condition-occurs
yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }

while getopts z: option
  do
  case "${option}"
    in
      z) CONFIG_FILE=${OPTARG};;
  esac
done

CONFIG_DEFAULT="DEFAULT"
CONFIG_FILE=${CONFIG_FILE:-$CONFIG_DEFAULT}
_python_script="daemon_args.py"

#https://stackoverflow.com/questions/59895/how-to-get-the-source-directory-of-a-bash-script-from-within-the-script-itself
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
_module_script="$DIR/$_python_script"

# which python is being used
py_name="$(which python)"
_default_pi_python="/home/pi/.conda/envs/aero/bin/python"
_default_laptop_python="/home/jackburdick/anaconda3/envs/aerodev/bin/python"

# which device is currently being used
_device_pi_name="pi"
_device_laptop_name="jackburdick"
_device_cur_name="$(whoami)"

# see if aeropi is installed
_aeropi_not_avail="$( python -c "import aeropi" 2>&1 )"
if [ -z _aeropi_not_avail ]; then
  # aeropi is not present
  
  # set python to the default python for the current device
  if [$_device_cur_name == $_device_pi_name]; then
    _py_cmd=$_default_pi_python
  else
    _py_cmd=$_default_laptop_python
  fi
else
  # aeropi is available in current python
  _py_cmd=$py_name 
fi


workerNames=()
workerArgs=()
i=0
while read line ; do
  if [ $i == 0 ]
    then
      workerNames+=$line
  elif [ $i == 1 ]
    then
      workerArgs+=$line
  else
    die "Too many lines recieved from $_module_script"
  fi
  ((++i))
done < <($_py_cmd $_module_script $configFile)
workerNames=($workerNames)
workerArgs=($workerArgs)


# iterate
for i in "${!workerNames[@]}"; do 
  printf "%s - %s - %s\n" "$i" "${workerNames[$i]}" "${workerArgs[$i]}"
done
