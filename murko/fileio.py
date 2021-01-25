import yaml
import json
import pickle
from pathlib import Path
from os import walk
from numpy import loadtxt


def ls(path):
	f = []
	d = []
	for (dirpath, dirnames, filenames) in walk(path):
		f.extend(filenames)
		d.extend(dirnames)
		break

	return (f, d)


def dump(obj, fname):
	"""
	Dumps a files to disc. Supported formats are `.yaml`, `.json`, 
	and everything else will be pickled.
	"""

	p = Path(fname)
	name   = p.stem 
	format = p.suffix

	

	if format==".yaml": 
		with open(p, 'w') as f:
			yaml.dump(obj, f, 
				allow_unicode=True, 
				sort_keys=False,
				indent=4,
				explicit_start=True)

	elif format==".json": 
		with open(p, 'w') as f:
			json.dump(obj, f, 
						indent=4)

	else:
		with open(p, 'wb') as f:
			pickle.dump(obj, f)


def load(fname):

	p = Path(fname)
	name   = p.stem 
	format = p.suffix


	if format==".yaml": 
		with open(p, 'r') as f:
			return yaml.load(f, Loader=yaml.FullLoader)

	elif format==".json": 
		with open(p, 'r') as f:
			return json.load(f)

	elif format==".pkl": 
		with open(p, 'rb') as f:
			return pickle.load(f)

	elif format==".txt": 
		with open(p, 'r') as f:
			lines = f.read().split('\n')
			return lines


def save_data(fname, data):
	with open(fname, "wb") as f:
		data = pickle.dump(data, f)


def load_data(fname, keys=None, path=None):
	if path is not None: fname = Path(path)/fname

	with open(fname, "rb") as f:
		data = pickle.load(f)

	if keys is None: return data
	else: return [data[k] for k in keys]