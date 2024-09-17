import logging
import os

from grid5000 import Grid5000


logging.basicConfig(level=logging.DEBUG)

conf_file = os.path.join(os.environ.get("HOME"), ".python-grid5000.yaml")
gk = Grid5000.from_yaml(conf_file)

# state=running will be placed in the query params
running_jobs = gk.sites["rennes"].jobs.list(state="running")
print(running_jobs)

# get a specific job by its uid
job = gk.sites["rennes"].jobs.get("424242")
print(job)
# or using the bracket notation
job = gk.sites["rennes"].jobs["424242"]
print(job)