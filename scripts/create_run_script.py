
import argparse
from murko.omx import create_run_script


parser = argparse.ArgumentParser(description='Creates run.sh...', 
						argument_default=argparse.SUPPRESS)
parser.add_argument('num_jobs', type=int)
parser.add_argument('arr_size', nargs="?", default=100,  type=int)
parser.add_argument('step', nargs="?", default=20,   type=int)
parser.add_argument('--dir', dest="target_dir", default="./", type=str, help='Where the script is created')
parser.add_argument('--name', dest="name", default="run.sh", type=str, help='Name of the run script')
parser.add_argument('--abbr', dest="job_abbr", default="omx", type=str, help='Abbreviation of job name on OM')
parser.add_argument('--script', dest="job_script", default="job.sh", type=str, help='The name of the job script that is run')
parser.add_argument('--templ', dest="templ", type=str, help='Path to the run.sh template.')


if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    create_run_script(**vars(args))