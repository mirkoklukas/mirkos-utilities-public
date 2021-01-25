#!/bin/sh

#SBATCH --job-name={{job_name}}
#SBATCH --time={{hours}}:{{mins}}:00
#SBATCH --partition={{partition}}
#SBATCH --mem-per-cpu={{mem_per_cpu}}
#SBATCH --mail-type=END
#SBATCH --mail-user={{mail_user}}
#SBATCH --out=io/out_%x_%a
#SBATCH --error=io/err_%x_%a
#SBATCH --exclude=node030,node016

source /etc/profile.d/modules.sh
module add openmind/singularity
export SINGULARITY_CACHEDIR=/om5/user/`whoami`/.singularity

export PYTHONPATH="${PYTHONPATH}:/omx"
export PYTHONPATH="${PYTHONPATH}:/om2/user/mklukas/om-experiments/mirkos-utilites"
export PYTHONPATH="${PYTHONPATH}:/om2/user/mklukas/om-experiments/"
{% for p in pypath %}export PYTHONPATH="${PYTHONPATH}:{{p}}"
{% endfor %}
singularity exec -B /om:/om,/om5:/om5,/om2:/om2,{{nbx_folder}}:/omx \
                                {{simg}} \
                                python {{script}} \
                                --job-id   $SLURM_ARRAY_JOB_ID \
                                --task-id  $SLURM_ARRAY_TASK_ID \
                                --results-dir {{results_dir}}