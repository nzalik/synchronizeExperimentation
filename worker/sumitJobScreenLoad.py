import json
import os
import requests
from time import sleep
import subprocess

#user = input(f"Grid'5000 username (default is {os.getlogin()}): ") or os.getlogin()
user = "ykoagnenzali "
password = "GPuVQr2G!Rw2YM9"
#password = ""
#password = input("Grid'5000 password (leave blank on frontends): ")
g5k_auth = (user, password) if password else None

site_id = "nantes"
cluster = "econome"

api_job_url = f"https://api.grid5000.fr/stable/sites/{site_id}/jobs"

payload = {
    "resources": "nodes=2,walltime=5:00",
    "command": "sleep infinity",
    "stdout": "api-test-stdout2",
    "properties": f"cluster='{cluster}'",
    "name": "load_constant"
}
job = requests.post(api_job_url, data=payload, auth=g5k_auth).json()
job_id = job["uid"]

sleep(60)
state = requests.get(api_job_url + f"/{job_id}", auth=g5k_auth).json()
print("information ssur le job")
print(json.dumps(state, indent=4))
# if state != "terminated":
#     # Deleting the job, because it takes too much time.
#     requests.delete(api_job_url+f"/{job_id}", auth=g5k_auth)
#     print("Job deleted.")

servers = state["assigned_nodes"]

print("the servers are")
print(servers)

server1 = f"{user}@{servers[0]}"
# Execute the previous script on server1
subprocess.run(["ssh", server1, "bash ./scripts/worker.sh"], check=True)

# Execute the deployment script on server2
#subprocess.run(["ssh", servers[1], "bash ./deployment.sh"], check=True)

