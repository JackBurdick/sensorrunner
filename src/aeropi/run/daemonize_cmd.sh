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
done < <(python $_module_script $configFile)
workerNames=($workerNames)
workerArgs=($workerArgs)


# iterate
for i in "${!workerNames[@]}"; do 
  printf "%s - %s - %s\n" "$i" "${workerNames[$i]}" "${workerArgs[$i]}"
done
