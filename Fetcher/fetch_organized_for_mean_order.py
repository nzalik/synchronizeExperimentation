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
            #query_str_file = os.path.join(directory2, filename)
            # if os.path.exists(query_str_file):
            #     base, ext = os.path.splitext(filename)
            #     counter = 1
            #     while os.path.exists(os.path.join(directory, f"{base}_{counter}{ext}")):
            #         counter += 1
            #     query_str_file = os.path.join(directory, f"{base}_{counter}{ext}")

            # query_str_file = "nom_du_fichier.json"
            os.makedirs(directory, exist_ok=True)

            try:
                res = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                    data=payload).json()

                if res != None and len(res['data']['result']) > 0:
                    with open(query_str_file, 'a') as f:
                        json.dump(res, f, ensure_ascii=False)

            except Exception as e:
                print(e)
                print("...Fail at Prometheus request.")


    container_name = "pod_info"

    query_str = "kube_deployment_status_replicas_ready{namespace=\"default\"}"
    query_str2 = f"sum(irate(container_cpu_usage_seconds_total{{namespace=\"default\", container!=\"\"}}[{cpu_step}])) by (container)"
    query_str3 = "sum(container_memory_usage_bytes{namespace=\"default\", container!=\"\"}) by (container)"
    query_str4 = "kube_pod_container_status_restarts_total{namespace=\"default\", container!=\"\"}"

    url = prom_url + '/api/v1/query_range?'

    payload = {'query': query_str, 'start': new_timestampManual, 'end': target_timeManual, 'step': step}
    payload2 = {'query': query_str2, 'start': new_timestampManual, 'end': target_timeManual, 'step': step}
    payload3 = {'query': query_str3, 'start': new_timestampManual, 'end': target_timeManual, 'step': step}
    payload4 = {'query': query_str4, 'start': new_timestampManual, 'end': target_timeManual, 'step': step}

    res = None

    directory2 = path_to_save(dir_name) + "/pod_info"
    directory3 = path_to_save(dir_name) + "/aggregation"

    os.makedirs(directory2, exist_ok=True)
    os.makedirs(directory3, exist_ok=True)

    # The name of the current experimentation file
    profile = dir_name.split('/')[-1]
    filename = f"{exp_nb}_{container_name}.json"
    filename2 = f'{exp_nb}_aggregation_{profile}.json'
    filename3 = f'{exp_nb}_aggregation_memory_{profile}.json'
    filename4 = f'{exp_nb}_pod_restart_{profile}.json'
    query_str_file = os.path.join(directory2, filename)

    query_str_file2 = os.path.join(directory3, filename2)
    query_str_file3 = os.path.join(directory3, filename3)
    query_str_file4 = os.path.join(directory3, filename4)
    
    # if os.path.exists(query_str_file2):
    #     base, ext = os.path.splitext(filename2)
    #     counter = 1
    #     while os.path.exists(os.path.join(directory3, f"{base}_{counter}{ext}")):
    #         counter += 1
    #     query_str_file2 = os.path.join(directory3, f"{base}_{counter}{ext}")
    # 
    # query_str_file3 = os.path.join(directory3, filename3)
    # if os.path.exists(query_str_file3):
    #     base, ext = os.path.splitext(filename3)
    #     counter = 1
    #     while os.path.exists(os.path.join(directory3, f"{base}_{counter}{ext}")):
    #         counter += 1
    #     query_str_file3 = os.path.join(directory3, f"{base}_{counter}{ext}")
    # 
    # query_str_file4 = os.path.join(directory3, filename4)
    # if os.path.exists(query_str_file4):
    #     base, ext = os.path.splitext(filename4)
    #     counter = 1
    #     while os.path.exists(os.path.join(directory3, f"{base}_{counter}{ext}")):
    #         counter += 1
    #     query_str_file4 = os.path.join(directory3, f"{base}_{counter}{ext}")

    # query_str_file = "nom_du_fichier.json"



    # if os.path.exists(query_str_file):
    #     base, ext = os.path.splitext(filename)
    #     counter = 1
    #     while os.path.exists(os.path.join(directory2, f"{base}_{counter}{ext}")):
    #         counter += 1
    #     query_str_file = os.path.join(directory2, f"{base}_{counter}{ext}")



    # Query Prometheus
    try:
        # res = requests.get(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}).json()
        res = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'},
                            data=payload).json()
        res2 = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'},
                            data=payload2).json()
        res3 = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'},
                            data=payload3).json()

        res4 = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'},
                             data=payload4).json()
        # print("la reponse pour les pods")
        # print(res)
        if res != None and len(res['data']['result']) > 0:
            with open(query_str_file, 'a') as f:
                json.dump(res, f, ensure_ascii=False)

        if res2 != None and len(res['data']['result']) > 0:
            with open(query_str_file2, 'a') as f:
                json.dump(res2, f, ensure_ascii=False)

        if res3 != None and len(res['data']['result']) > 0:
            with open(query_str_file3, 'a') as f:
                json.dump(res3, f, ensure_ascii=False)

        if res4 != None and len(res['data']['result']) > 0:
            with open(query_str_file4, 'a') as f:
                json.dump(res4, f, ensure_ascii=False)

    except Exception as e:
        print(e)
        print("...Fail at Prometheus request.")

