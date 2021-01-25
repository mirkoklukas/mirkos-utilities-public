#!/usr/bin/env python
from os import makedirs
from pathlib import Path
from argparse import ArgumentParser
parser = ArgumentParser(description='Wraps an experiment...')
parser.add_argument('--job-id', dest="job_id", default=0, type=int)
parser.add_argument('--task-id', dest="task_id", default=0, type=int)
parser.add_argument('--results-dir', dest="results_dir", default=Path(__file__).parent/'results', type=str)


def run(job_id, task_id, results_dir):
	pass


if __name__ == '__main__':
	args = parser.parse_args()
	
	j  = args.job_id
	t  = args.task_id
	rd = Path(args.results_dir)/f"{t}"

	makedirs(rd, exist_ok=True)
	
	run(job_id=j, task_id=t, results_dir=rd)