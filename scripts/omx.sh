DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

######
if [[ "$1" == "run" ]]
then
  python $DIR/create_run_script.py ${@:2}
fi

######
if [[ "$1" == "job" ]]
then
  python $DIR/create_job_script.py ${@:2}
fi

######
if [[ "$1" == "exp" ]]
then
  python $DIR/create_exp_script.py ${@:2}
fi