# imports - standard imports
import os, os.path as osp
from   functools import partial
import sys

# imports - module imports
from sbml2json.config          import PATH, Settings
from sbml2json.util.imports    import import_handler
from sbml2json.util.system     import popen
from sbml2json.util._dict      import merge_dict
from sbml2json.util.environ    import getenvvar, getenv
from sbml2json import parallel, log

settings = Settings()
logger   = log.get_logger()

JOBS = [
    
]

def run_job(name, variables = None):
    job = [job for job in JOBS if job["name"] == name]
    if not job:
        raise ValueError("No job %s found." % name)
    else:
        job = job[0]

    variables = merge_dict(job.get("variables", {}), variables or {})

    popen("%s -c 'from sbml2json.util.imports import import_handler; import_handler(\"%s\")()'" %
        (sys.executable, "sbml2json.jobs.%s.run" % name), env = variables)

def run_all():
    logger.info("Running all jobs...")
    for job in JOBS:
        if not job.get("beta") or getenv("JOBS_BETA"):
            run_job(job["name"], variables = job.get("variables"))