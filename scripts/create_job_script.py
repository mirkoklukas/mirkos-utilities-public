import argparse
from murko.omx import create_job_script


parser = argparse.ArgumentParser(description='Creates a job.sh...',
	argument_default=argparse.SUPPRESS)
parser.add_argument('--dir', dest="target_dir", default="./", type=str, help='Where the script is created')
parser.add_argument('--name', dest="name", default="job.sh", type=str, help='Name of the job script')
parser.add_argument('--script', dest="script", default="experiment.py", type=str, help='The name of the python experiment.')
parser.add_argument('--templ', dest="templ", type=str, help='Path to the run.sh template.')
parser.add_argument('-pp', '--pypath', dest="pypath", type=str, help='Path to the run.sh template.')


if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    if 'pypath' in args:
    	args.pypath = args.pypath.split(",")
    	# print(args.pypath.split(","))
    create_job_script(**vars(args))