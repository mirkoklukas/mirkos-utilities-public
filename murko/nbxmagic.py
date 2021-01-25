"""
Collection of jupyter notebook magic functions.
To use them you have to load the module and call

	'%load_ext murko.nbxmagic'

in your notebook
"""
from murko.config import ConfigSpace
import re


re_xarg = re.compile(r"""
^
([^=]+)
=
([^;]+)
;?
([^;]*)
;?
([^;]*)
$""", re.VERBOSE)


def strip(s):
	return s.strip()


def parse_xarg(line):
	m = re_xarg.match(line)
	if m is not None:
		name, val, sweep, label = map(strip, m.groups())

		abbr = None
		in_label = False
		if len(sweep) == 0: sweep = f"[{val}]"

		if len(label) > 0:
			if label[0] == "+": 
				in_label = True
				abbr = label[1:]

			elif label[0] == "-":
				in_label = False
				abbr = label[1:]

			else:
				in_label = False
				abbr = label


		return name, val, sweep, abbr, in_label
	else: 
		return None
	

def xconf(line, cell, local_ns):	

	args = line.split()
	fname = args[0]
	local_conf_name = None
	if len(args) > 1:
		local_conf_name = args[1]

	ps = ConfigSpace(fname)

	for line in cell.strip().split('\n'):
		line = line.strip()
		if len(line) == 0: continue

		key, val, sweep, abbr, do_attach = parse_xarg(line)
		ps.add(key, eval(sweep), abbr, do_attach)



	if local_conf_name is not None:
		local_ns.update({local_conf_name: ps[0]})


	if len(ps) == 1:
		ps[0].fname = fname
		ps[0].dump(fname)


		return ps[0]

	else:
		ps.dump()
		return ps


xconf.needs_local_scope = True


def load_ipython_extension(ipython):
		"""This function is called when the extension is
		loaded. It accepts an IPython InteractiveShell
		instance. We can register the magic with the
		`register_magic_function` method of the shell
		instance."""
		ipython.register_magic_function(xconf, 'cell')