
import argparse 
from murko.omx import create_exp_script

parser = argparse.ArgumentParser(description='Creates a python exp...',
			argument_default=argparse.SUPPRESS)
parser.add_argument('--dir', dest="target_dir", default="./", type=str, help='Where the script is created')
parser.add_argument('--name', dest="name", default="experiment.py", type=str, help='Name of the python script')
parser.add_argument('--templ', dest="templ", type=str, help='Path to the exp template.')


if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    create_exp_script(**vars(args))