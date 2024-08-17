import json
import os
import requests
from time import sleep
import subprocess

#user = input(f"Grid'5000 username (default is {os.getlogin()}): ") or os.getlogin()
user = "ykoagnenzali"
#password = "GPuVQr2G!Rw2YM9"
password = ""

admin = "root"
#password = ""
#password = input("Grid'5000 password (leave blank on frontends): ")
g5k_auth = (user, password) if password else None

site_id = "nantes"
cluster = "econome"

api_job_url = f"https://api.grid5000.fr/stable/sites/{site_id}/jobs"

payload = {
    "resources": "nodes=2,walltime=0:05",
    "command": "sleep infinity",
    "stdout": "api-test-stdout2",
    "properties": f"cluster='{cluster}'",
    "name": "load_constant1"
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
worker_script_path = "./scripts/worker.sh"
#deployment_script_path = "../Generator/deploy_group_scaling.sh"
deployment_script_path = "../Generator/auto/simple.sh"
print("the servers are")
print(servers)

# Define server with f-string (safe for variable substitution)
server1 = f"{user}@{servers[0]}"
server2 = f"{user}@{servers[1]}"

# Execute the script on server1 using SSH (more secure)

worker = subprocess.run([worker_script_path, server1], capture_output=True, text=True)

print(worker.stdout)
#print("en cas deerrer")
#print(worker.stderr)

# Deployment here

deployment = subprocess.run([deployment_script_path, server2, servers[0]], capture_output=True, text=True)

print("#########################")
print(deployment.stdout)
print("en cas dereru")
print(deployment.stderr)
# Execute the deployment script on server2
#subprocess.run(["ssh", servers[1], "bash ./deployment.sh"], check=True)
