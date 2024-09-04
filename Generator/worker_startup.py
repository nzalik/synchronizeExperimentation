import json
import os
import requests
from time import sleep
import sys

#user = input(f"Grid'5000 username (default is {os.getlogin()}): ") or os.getlogin()
user = "ykoagnenzali"
#password = "GPuVQr2G!Rw2YM9"
password = ""

admin = "root"
#password = ""
#password = input("Grid'5000 password (leave blank on frontends): ")
g5k_auth = (user, password) if password else None

site_id = sys.argv[1] #"nantes"
cluster = sys.argv[2] #"econome"

api_job_url = f"https://api.grid5000.fr/stable/sites/{site_id}/jobs"

payload = {"resources": "nodes=1,walltime=5:00",
           "command": "sleep infinity",
           "stdout": "api-test-stdout2",
           "properties": f"cluster='{cluster}'",
           "name": f"{site_id}-{cluster}"
           }
job = requests.post(api_job_url, data=payload, auth=g5k_auth).json()
job_id = job["uid"]

sleep(20)
state = requests.get(api_job_url + f"/{job_id}", auth=g5k_auth).json()

# if state != "terminated":
#     # Deleting the job, because it takes too much time.
#     requests.delete(api_job_url+f"/{job_id}", auth=g5k_auth)
#     print("Job deleted.")

servers = state["assigned_nodes"]
worker_script_path = "../worker/scripts/worker.sh"
#deployment_script_path = "../Generator/deploy_group_scaling.sh"
deployment_script_path = "./deploy_group_scaling.sh"

# Define server with f-string (safe for variable substitution)
#server1 = f"{user}@{servers[0]}"
#server2 = f"{user}@{servers[1]}"

# Execute the script on server1 using SSH (more secure)

#worker = subprocess.run([worker_script_path, server1], capture_output=True, text=True)

print(servers[0])
