"""
A config is a nested (tree-like) dict 
with additional functionality, e.g. 
lookup with by colon separated keys 
to access the nested structure

A parameter space stores associations between 
colon separated keys and iterables. It is iterable 
with items being nested configs...
"""
import yaml
import numpy as np
import json
from murko.fileio import dump, load
from pathlib import Path
from murko.bunch import Bunch



def update_nested_dict(d, key, val):
    """
    Update a nested dict with a 
    colon separated key and value
    """
    splits = key.split(":")
    key  = splits[0]
    rest = ":".join(splits[1:])
    if len(rest) == 0: 
        d[key] = val
    else:
        if key not in d: d[key] = {} 
        update_nested_dict(d[key], rest, val)

    return d


def has_key(c,k):
    """Check if a colon separated key is present"""
    if k in c:
        return True
    else:
        splits = k.split(':')
        k0, k1 = splits[0], ':'.join(splits[1:])
        if len(k1) == 0: return False
        else:            return has_key(c[k0], k1)

def get_val(c,k):
    """Get a value from nested dict, 
    given a colon separated key"""
    if k in c:
        return c[k]
    else:
        splits = k.split(':')
        k0, k1 = splits[0], ':'.join(splits[1:])
        if len(k1) == 0: return None


        return get_val(c[k0], k1)


def get_items(c): 
    """
    Get items with colon separated
    keys from nested dict
    """
    items = []
    for k,v in c.items():
        if type(v) is dict:
            items.extend([(":".join([k,k_]),v_)
                for k_,v_ in get_items(v)])
        else: 
            items.append((k,v))

    return items


def get_values(c):
    """Get values from nested dict"""
    items = get_items(c)
    return [v for (k,v) in items]


def get_leaves(c):
    """Get values from nested dict"""
    items = get_items(c)
    return [(k.split(':')[-1],v) for (k,v) in items]


def get_keys(c):
    """Get colon separated keys from nested dict"""
    items = get_items(c)
    return [k for (k,v) in items]


def flatten(d):
    return dict(get_items(d))


def bunch(d):
        b = Bunch()
        for k,v in d.items():
            if type(v) is dict:
                b[k] = bunch(v)
            else:
                b[k] = v
        return b


def nest(d):
    """
    Create nested dict from dict 
    with colon separated keys
    """
    nested = {}
    for k,v in d.items():
        update_nested_dict(nested, k, v)

    return nested 


def label_from_leaves(d, attach=[], abbr={}, asignment="_", separation="_"):
    """
    Create a label from the leaves of a nested dict `d`,
    if the leaf's name is in `attach`.
    """
    labels = []
    for k,v in get_items(d):
        k_ = k.split(':')[-1]

        if k in abbr: k_ = abbr[k]


        if k in attach:
            labels.append(f"{k_}{asignment}{v}")
            

    return f"{separation.join(labels)}"


def config_label(d):
    return label_from_leaves(d)


def load_conf(fname):
    d = load(fname)
    return flatten(d)


def dump_flat(c, fname):
    dump(flatten(c), fname)


def dump_nested(c, fname):
    dump(nest(c), fname)



def needs_local_scope(func):
    func.needs_local_scope = True
    return func




def is_lambda_str(val):
    return type(val) == str and val[:6] == "lambda"


def is_basically_a_function(val):
    return hasattr(val, '__call__') or is_lambda_str(val)
               

def is_basically_a_list(val):
    return hasattr(val, '__iter__') and type(val) != str


def replace_maybe(k, abbr):
    if k in abbr: return abbr[k]
    else: return k



#####################################################
#####################################################
#####################################################
#####################################################
#####################################################
#####################################################
#####################################################



class Config(dict):
    """
    A config is a nested (tree-like) dict 
    with additional functionality.
    """
    def __init__(self, fname=None):
        super().__init__()
        self.fname  = fname
        self.attach = []
        self.abbr   = {}


    def __getitem__(self, k):
        if not has_key(self.nested, k): raise Exception("Key error")
        return get_val(self.nested, k)


    def __setitem__(self, key, val):
        """ Allows for access with colon separated keys"""            
        super().update(
            update_nested_dict(self.nested, key, val))


    @property
    def name(self):
        return Path(self.fname).stem


    @property    
    def leaves(self):
        leaves = []
        for key , v in get_items(self):
            key = replace_maybe(key, self.abbr) 
            key = key.split(':')[-1]
            leaves.append((key,v))

        return leaves


    @property    
    def nested(self):
        return nest(self)


    @property
    def bunch(self):
        return bunch(self.nested)
    

    @property
    def flattened(self):
        return flatten(self)


    def from_loaded(self, c):
        self.attach = get_val(c, 'state:attach') or []
        self.abbr   = get_val(c, 'state:abbr') or {}
        super().update(get_val(c, 'dictitems') or c)


    def dump(self, fname=None):
        if fname is None: 
            p = Path(self.fname)
        else:
            if len(Path(fname).suffix)==0: #fname is a path
                if self.fname is None: raise Exception("No filename...")
                p = Path(fname)/Path(self.fname).name
            else:
                p = Path(fname)

        dump({'state': {'attach': self.attach, 'abbr': self.abbr}, 
              'dictitems': self.nested }, p)

        return p


    def load(self, fname):
        d = load(fname)
        self.fname= fname
        self.from_loaded(d)
        return self


    def update_ns(self, ns):
        """Adds the config's leaves to namespace 
        with abbreviation if present"""
        ns.update(self.leaves)


    @property
    def label(self):
        return self.get_label(self.attach, self.abbr)


    def set_label(self, attach, abbr=None):
        self.attach = attach
        if abbr is not None: self.abbr = abbr
        return self.label


    def get_label(self, attach=None, abbr=None, asignment="", separation="_"):
        return label_from_leaves(self, 
                    attach=attach, 
                    abbr=abbr, 
                    asignment=asignment, 
                    separation=separation)

  


    def __str__(self):
        s = f"Config({{\n"
        if self.fname is not None: 
                s = f"{self.fname}:Config({{\n"
        items = []
        for k,v in get_items(self):
            k_ =f"'{k}'"
            items.append(f"  {k_}\t : {v}")
        s += ",\n".join(items)
        s += "\n})"
        return s

    def __repr__(self):
        return str(self)



#####################################################
#####################################################
#####################################################
#####################################################
#####################################################
#####################################################
#####################################################


class ConfigSpace(object):
    def __init__(self, fname="", order="col"):
        self.set_order(order)
        self.fname  = fname
        self.shape  = ()
        self.keys   = []
        self.vals   = []
        self.abbr   = {}
        self.attach = [] # attach to label


    def add(self, key, vals, abbr=None, attach=False):
        if key in self.keys: 
            raise Exception(f"Key `{key}` already in there....") 
        if not (is_basically_a_list(vals) or is_lambda_str(vals)): 
            raise Exception(f"Values `{vals}` should be iterable or a special lambda str...")


        if is_lambda_str(vals): 
            self.shape += (1,)
        else:
            vals = list(vals)
            self.shape += (len(vals),)

        self.keys.append(key)
        self.vals.append(vals)
        if attach: self.attach.append(key)
        if abbr is None or abbr == "": abbr = key.split(":")[-1]
        self.abbr[key]= abbr
    
        return self


    def __getitem__(self, i):
        if type(i) == int:
            assert i < len(self), f"{i} = key >= length = {len(self)}"
            return self.get_config(i)
        else:
            raise Exception("Get can only handle integer keys atm...")


    def get_config(self, t):

        p    = Path(self.fname)
        conf = Config(f"{p.stem}_{t}{p.suffix}")
        conf.abbr   = self.abbr
        conf.attach = self.attach


        func_items = []
        I = self.get_multi_index(t)
        for k, i in enumerate(I):

            key   = self.keys[k]
            vals  = self.vals[k] 

            if is_basically_a_list(vals):
                conf[key] = vals[i]
            else:
                # Handling dynamic Values later
                func_items.append((key,vals))


        # Finally handling dynamic Values
        for k,f in func_items:
            if is_lambda_str(f):
                v = eval(f"({f})()", conf.bunch)
                conf[k] = v
            else: raise Exception("Can't handle `{f}`")

        return conf


    def __len__(self):
        if len(self.shape)>0: return np.product(self.shape)
        else: return 0

    
    def __iter__(self):
        self._i = 0
        return self


    def __next__(self):
        if self._i < len(self):
            p = self[self._i]
            self._i += 1
            return p
        else:
            raise StopIteration


    @property
    def dim(self):
        return len(self.shape)


    @property
    def nested(self):
        d = {}
        for k,v in zip(self.keys, self.vals):
            update_nested_dict(d, k, v)

        return d

    def get_multi_index(self, t):
        """
        “Row-major” ordering is also referred to as “C-ordering” 
        because this is the traversal method utilized in the C language. 
        “Column-major” ordering, on the other hand, is also referred to as “F-ordering”, 
        because it is used by the Fortran language.
        """
        shape = self.shape
        order = self.order
        n = len(shape)
        I = [None]*n
        for k in range(0,n):
            if order == "row": 
                i = t//np.prod(shape[k+1:])
                I[k] = int(i)%shape[k]
            if order == "col":
                i = t//np.prod(shape[:k])
                I[k] = int(i)%shape[k]

        return I

    def coords(self, c):
        I = [None]*len(self.shape)
        assert isinstance(c, dict)

        for k,v in get_items(c):
            j = self.keys.index(k)
            vals = self.vals[j]

            if is_lambda_str(vals):
                if v == eval(f"({vals})()", bunch(c)):
                    I[j] = 0
                else:
                    raise Exception(f"can't find this config in here: {key}={v}")
            else:
                if vals.index(v) >=0:
                    I[j] = vals.index(v)
                else:
                    raise Exception(f"can't find this config in here: {key}={v}")

        return I


    def find(self, c):
        assert isinstance(c, dict)
        I = self.coords(c)

        t = 0
        for j,i in enumerate(I):
            t += i*np.prod(self.shape[j+1:])

        return int(t)


    def show_2dgrid(self, k=None, l=None):
        k,l = self.keys[:2]
        i,j = self.keys.index(k), self.keys.index(l)
        a,b = self.abbr[:2]

        grid = np.stack(np.meshgrid(self.vals[j], self.vals[i]),axis=2)
        print(f"--- ({a} {b}):\n")
        for i,row in enumerate(grid):
            s = '  '.join(["{:10s}".format(str(c)[:10]) for c in row])
            print(s)
        print("\n---")


    def __str__(self):
        s = f"ConfigSpace({{\n"
        if self.fname is not None: 
                s = f"{self.fname}:ConfigSpace({{\n"
        items = []
        for k,v in zip(self.keys, self.vals):
            k_ =f"'{k}'"
            items.append(f"  {k_}\t : {v}")
        s += ",\n".join(items)
        s += "\n})"
        return s


    def __repr__(self):
        return str(self)


    def sample(self):
        t = np.random.choice(len(self))
        x = self[t]
        return x


    def set_order(self, order):
        """
        Sets the order of traversal of the parameter array.
        Note that the first dimension is the "column" (col) direction,
        and the second dimension is the "row" direction.
        """
        assert order == "col" or order == "row"
        self.order = order


    def dump(self, fname=None):
        assert fname is not None or self.fname is not None

        if fname is None: 
            fname = self.fname


        dump({
            'state': {
                'len': len(self),
                'attach': self.attach,
                'abbr': self.abbr}, 
            'dictitems': self.nested
        }, fname)

        return fname


    def load(self, fname):
        d = load(fname)
        self.fname= fname
        self.from_loaded(d)

        return self


    def from_loaded(self, d):
        assert has_key(d, 'state') and has_key(d, 'dictitems')

        for k, vals in get_items(d['dictitems']):

            # This enables to load a single config 
            # as a 1-element space
            if not is_basically_a_function(vals):
                if not hasattr(vals, '__iter__') or type(vals) == str:
                    vals = [vals]
            else:
                if not is_lambda_str(vals):
                    raise Exception("can only handle special lambda strings atm")

            self.add(k, vals)

        self.attach = d['state']['attach']
        self.abbr   = d['state']['abbr']

    
    