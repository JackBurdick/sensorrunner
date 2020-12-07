#!/bin/bash

# https://stackoverflow.com/questions/1378274/in-a-bash-script-how-can-i-exit-the-entire-script-if-a-certain-condition-occurs
yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }

#outputString=$(python some_python.py "from_bash")
# myarr=()
# i=0
# python some_python.py "from_bash" | while read line ; do
#     echo $line
#     #myarr[i]=$line
#     #echo "insert"
# done

pythonScript="daemon_args.py"
configFile="some_config_path_to_send_to_python"

workerNames=()
workerArgs=()
i=0
while read line ; do
  if [ $i -eq 0 ]
    then
      workerNames+=$line
  elif [ $i == 1 ]
    then
      workerArgs+=$line
  else
    die "Too many lines recieved from $pythonScript"
  fi
  ((++i))
done < <(python $pythonScript $configFile)


echo ${workerNames}
echo ${workerArgs}

#echo "$outputString"

# # convert to array
# namesArr=($outputString)

# # iterate
# for i in "${!outputString[@]}"; do 
#   printf "%s - %s\n" "$i" "${outputString[$i]}"
# done