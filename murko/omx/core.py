from pathlib import PurePosixPath as Path
import pkg_resources
import os
import importlib
from murko.templ import create_file_from_template

# -------------------------
# That should be the 
# path to all the templates
tpath = Path(pkg_resources.resource_filename(__name__, "./"))


def get_interval_bounds(num, step=1000):
    if num < step: return [[1,num]]

    arrays = []
    for i in range(num//step): arrays.append([1, step])
    last = arrays[-1][1]
    if num%step!=0: arrays.append([1,num%step])
    return arrays


def get_specs_array(job_arrays, arr_size):
  return [[j]+job_arrays[j]+[j*arr_size] for j in range(len(job_arrays))]




def create_run_script(num_jobs=1, arr_size=100, step=20,  
                            target_dir="./",
                            job_abbr="omx", 
                            job_script="job.sh", 
                            name="run.sh", 
                            templ=tpath/"run.tpl"):

    assert arr_size <= 1000, "Maximum number of queued jobs on OM is 1000"


    job_arrays = get_interval_bounds(num_jobs, arr_size)

    fname = Path(target_dir)/name

    create_file_from_template(templ, fname, {
        'specs_array': get_specs_array(job_arrays, arr_size),
        'job_name'   : job_abbr,
        'job_script' : job_script,
        'step'       : step
    })


def create_job_script(
            target_dir="./", 
            name="job.sh", 
            script="experiment.py",
            templ=tpath/"job.tpl",
            pypath=[]):
  
    fname = Path(target_dir)/name

    create_file_from_template(templ, fname, {
        'job_name': 'omx',
        'script': script,
        'hours': 0,
        'mins': 30,
        'mem_per_cpu': "4GB",
        'partition': "fiete",
        'simg': "/om2/user/mklukas/simg/pytorch.simg",
        'nbx_folder': "/om2/user/mklukas/om-experiments",
        'results_dir': "results",
        'pypath': pypath
    })


def create_exp_script(target_dir="./", name="experiment.py", templ=tpath/"experiment.tpl"):
  
    fname = Path(target_dir)/name
    create_file_from_template(templ, fname, {})