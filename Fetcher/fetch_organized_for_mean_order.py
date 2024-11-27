import sys
import requests
import json
from datetime import datetime, timedelta, date
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
print(f"Parent Directory: {parent_dir}")

sys.path.append(parent_dir)  # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils')))

from utils.constants import (read_ini_file, query_svc_names, path_to_save,
                             step, cpu_step, init_metric_metadata)

file_path_init = f"{parent_dir}/config.ini"

string_argument = ""
repo_argument = ""
complete_storage_dir = ""
formattedDate=""

if len(sys.argv) > 1:
    string_argument = sys.argv[1]
    repo_argument = sys.argv[2]
    complete_storage_dir = sys.argv[3] #linear or constant
    formattedDate = sys.argv[4]

prom_url = sys.argv[5]
duration = sys.argv[6]
exp_nb = sys.argv[8]

print("la valeur de i")
print(exp_nb)

today = date.today()
date_str = today.strftime("%d-%m-%Y")

dir_name = f"{complete_storage_dir}"

if not os.path.exists(dir_name):
    os.makedirs(dir_name)

config = read_ini_file(file_path_init)

prometheus_url = prom_url + "/api/v1/query?query="

responses = {}

requetes_section = config['requetes']

csv_file_path = f"{repo_argument}/{string_argument}"

formatted_timestamp = formattedDate

current_date = datetime.now().strftime('%Y-%m-%d')

date_list = [
    f"{current_date} {formatted_timestamp}",
    ]

start_datetime_str=date_list[0]
#for start_datetime_str in date_list:

start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S")
start_timestamp = start_datetime.timestamp()

end_datetime = start_datetime + timedelta(minutes= int(duration))

end_timestamp = end_datetime.timestamp()

new_timestampManual = start_timestamp
target_timeManual = end_timestamp

all_services = query_svc_names("default",new_timestampManual, target_timeManual, prom_url)
#all_services = query_svc_names("default",target_timeManual, new_timestampManual, prom_url)
print("all services")
print(all_services)

pod_names  = [(svc["pod"]) for svc in all_services]
#services_names = ['-'.join(svc["pod"].split('-')[:-2]) for svc in all_services]

for section_name in config.sections():
    directory = ""
    for key, value in config.items(section_name):

        for svc in pod_names:

            root_container_name = '-'.join(svc.split('-')[:-2])

            directory = path_to_save(dir_name) + "/" + key + "/" + root_container_name

            container_name = svc

            query_str = init_metric_metadata(value, container_name, prom_url)

            #payload = {'query': query_str, 'start': new_timestamp, 'end': current_timestamp, 'step': step}
            payload = {'query': query_str, 'start': new_timestampManual, 'end': target_timeManual, 'step': step}

            url = prom_url + '/api/v1/query_range?'

            res = None

            filename = svc + '.json'
            query_str_file = os.path.join(directory, f"{exp_nb}_{filename}")

            os.makedirs(directory, exist_ok=True)
            print("fectch")
            print(url)
            try:
                res = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                    data=payload).json()

                if res != None and len(res['data']['result']) > 0:
                    with open(query_str_file, 'a') as f:
                        json.dump(res, f, ensure_ascii=False)

            except Exception as e:
                print(res)
                print(e)
                print("...Fail at Prometheus request.")

# Informations générales
container_name = "pod_info"
url = prom_url + '/api/v1/query_range?'

queries = [
    ("kube_deployment_status_replicas_ready{namespace=\"default\"}", "pod_info"),
    (
    f"sum(rate(container_cpu_usage_seconds_total{{namespace=\"default\", container!=\"\"}}[{cpu_step}])) by (container)",
    "aggregation_cpu"),
    ("sum(container_memory_usage_bytes{namespace=\"default\", container!=\"\"}) by (container)",
     "aggregation_memory"),
    ("kube_pod_container_status_restarts_total{namespace=\"default\", container!=\"\"}", "pod_restart"),
    (f"topk(64, sum(rate(container_cpu_usage_seconds_total{{namespace=\"default\"}}[{cpu_step}])) by (pod))",
     "top_pods"),
    (
    f"topk(64, histogram_quantile(0.95, sum(rate(istio_request_duration_milliseconds_bucket{{namespace=\"default\"}}[{cpu_step}])) by (le, destination_workload)))",
    "top_latencies"),
    (
    f"topk(64, sum(rate(istio_requests_total{{namespace=\"default\"}}[{cpu_step}])) by (destination_workload))",
    "top_requests")
]

payload_common = {
    'start': new_timestampManual,
    'end': target_timeManual,
    'step': step
}

# Création des dossiers
directory2 = path_to_save(dir_name) + "/pod_info"
directory3 = path_to_save(dir_name) + "/aggregation"

os.makedirs(directory2, exist_ok=True)
os.makedirs(directory3, exist_ok=True)

# Fichiers à générer
profile = dir_name.split('/')[-1]

try:
    for idx, (query_str, file_suffix) in enumerate(queries):
        payload = {'query': query_str, **payload_common}
        response = requests.post(
            url,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=payload
        ).json()

        # Vérifier et enregistrer les résultats
        if response and 'data' in response and response['data']['result']:
            filename = f"{exp_nb}_{file_suffix}_{profile}.json"
            directory = directory2 if file_suffix == "pod_info" else directory3
            filepath = os.path.join(directory, filename)

            with open(filepath, 'a') as f:
                json.dump(response, f, ensure_ascii=False)

except Exception as e:
    print(e)
    print("...Fail at Prometheus request.")
