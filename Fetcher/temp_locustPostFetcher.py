import csv
import sys
import requests
import configparser
import json
from datetime import datetime, timedelta, date
import os
import matplotlib.pyplot as plt
import time

string_argument = ""
repo_argument = ""
complete_storage_dir = ""
formattedDate=""

if len(sys.argv) > 1:
    string_argument = sys.argv[1]
    repo_argument = sys.argv[2]
    complete_storage_dir = sys.argv[3] #linear or constant
    formattedDate = sys.argv[4]

    print(string_argument)
    print(repo_argument)

file_path = '../teastore_grenoble.json'

def process_csv_line(csv_file):
    """
    Extrait la première ligne d'un fichier CSV, applique le traitement et renvoie le résultat.

    Args:
        csv_file (str): Chemin du fichier CSV.

    Returns:
        str: Timestamp formaté.
    """

    print("process sur le csv position")
    print(csv_file)
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        # Récupérer la première ligne
        line = next(reader)

    # Appliquer le traitement sur la première ligne
    fields = line[-1].split(';')
    date_str, time_str = fields[0].split(',')[-1].strip(), fields[1]

    # Formater le timestamp
    date_obj = datetime.strptime(date_str, '%d.%m.%Y')
    time_obj = datetime.strptime(time_str, '%H:%M')
    timestamp_formatted = time_obj.strftime('%H:%M')[:-3]

    print("dans un premier temps")
    print(timestamp_formatted)

    return timestamp_formatted
def read_ini_file(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def path_to_save(init_path):
    output_path = f"{init_path}/experimentation-{string_argument}"
    if os.path.exists(init_path):
        # Construire le nouveau nom de répertoire
        new_dir_name = f"data_{datetime.now().strftime('%H')}"
        output_path = f"{init_path}/experimentation-{string_argument}"

        if not os.path.exists(init_path):
            os.makedirs(init_path)

    return output_path

def get_timestamp(time_str, date_str=None):
    """
    Converts a date and time string to a timestamp.

    Args:
        date_str (str, optional): The date string in the format "YYYY-MM-DD". If not provided, the current date will be used.
        time_str (str): The time string in the format "HH:MM:SS.fff".

    Returns:
        float: The timestamp.
    """
    if date_str is None:
        date_str = date.today().strftime("%Y-%m-%d")

    datetime_str = date_str + " " + time_str
    dt_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    timestamp = dt_obj.timestamp()
    return timestamp

def read_parameters_from_json(file_path):
    with open(file_path, 'r') as file:
        parameters = json.load(file)
    return parameters

def query_prometheus(query):
    my_url = prom_url + '/api/v1/' + query
    res = None

    try:
        res = requests.get(my_url).json()
    except Exception as e:
        print(e)

    if res != None and 'error' in res:
        res = None

    return res

def query_prometheus_with_payload(prometheus_url, query, start_dt, end_dt, step):
    #payload = {'query': query, 'start': start_dt, 'end': end_dt, 'step': step + 's'}
    payload = {'query': query, 'start': start_dt, 'end': end_dt, 'step': step}

    url = prometheus_url + '/api/v1/query_range?'
    print("Querying " + url + " with payload " + str(payload))
    res = None

    # Query Prometheus
    try:
        res = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload).json()
    #    print(res)
    except Exception as e:
        print(e)
        print("...Fail at Prometheus request.")

    if res != None and 'error' in res:
        print(res["error"])
        res = None

    return res

def query_svc_names(namespace='default', start_dt="", end_dt=""):
    #query_str = 'label/pod/values?match[]=kube_pod_container_info{namespace="' + namespace + '"}'
    query_str = 'label/pod/values?match[]=kube_pod_container_info{namespace="' + namespace + '"}&start=' + str(
        start_dt) + '&end=' + str(end_dt)
    res = query_prometheus(query_str)
    services = []
    if res != None:
        svc_names = res['data']
        for name in svc_names:
            # query_str = '/query?query=container_last_seen{namespace="' + namespace + '", pod="' + name + '"}'
            query_str = 'container_last_seen{namespace="' + namespace + '", pod="' + name + '"}'
            res = query_prometheus_with_payload(prom_url, query_str, start_dt, end_dt, step)
            if res != None and len(res['data']['result']) > 0:
                instance = res['data']['result'][0]['metric']['instance'].split(':')[0]
                # node = res['data']['result'][0]['metric']['node']
                service_obj = {'pod': name, 'instance': instance}
                services.append(service_obj)

    return services



parameters = read_parameters_from_json(file_path)
valueTime = parameters['DURATION']
unit = parameters['DURATION_UNIT']
load = parameters['DURATION']

loop_limit = 0

if unit == "minutes":
    loop_limit = int(valueTime)
else:
    loop_limit = int(valueTime*60)

window = 6
window2 = 12

prom_url = parameters['PROMETHEUS_URL']

today = date.today()
date_str = today.strftime("%d-%m-%Y")

#dir_name = f"../nantes/hyperthreading/{category}/{date_str}/data/metrics"
dir_name = f"{complete_storage_dir}/data/metrics"

#dir_name = today.strftime("%d-%m-%Y")

#save_path = f"../{dir_name}"  #The directory where you want things to be saved

if not os.path.exists(dir_name):
    os.makedirs(dir_name)

cpu_step = "2m"
step = "1s"
def _init_metric_metadata(metric, pod_name):

    query_str = 'metadata?metric=' + metric
    url = prom_url + '/api/v1/' + query_str

    res = None

    root_container_name = '-'.join(pod_name.split('-')[:-2])

    print("le nom du pod")
    print("le nom du service")
    print(root_container_name)


    try:
        res = requests.get(url).json()
    except Exception as e:
        print(e)

    if res != None and 'error' in res:
        print(res["error"])
        res = None
    elif res != None and res['data']:
        metadata = res['data'][metric][0]

        if (metadata['type'] == "gauge"):
            return f"{metric}{{namespace=\"default\",pod=\"{pod_name}\", container=\"{root_container_name}\" }}"
        elif (metadata['type'] == "counter"):
            return f"irate({metric}{{namespace=\"default\",pod=\"{pod_name}\", container=\"{root_container_name}\"}}[{cpu_step}])"
        else:
            return f"{metric}{{namespace=\"default\"}}"




file_path = '../config.ini'
config = read_ini_file(file_path)

prometheus_url = prom_url + "/api/v1/query?query="

# Créer un dictionnaire pour stocker les réponses
responses = {}

# Obtenir la section 'requetes' du fichier de configuration
requetes_section = config['requetes']

# Chemin vers le csv que je viens de générer apres injection de charges
csv_file_path = f"{repo_argument}/{string_argument}"

print("le chemin pour aller")
print(csv_file_path)

#formatted_timestamp = process_csv_line(csv_file_path)
formatted_timestamp = formattedDate

current_date = datetime.now().strftime('%Y-%m-%d')

date_list = [
    f"{current_date} {formatted_timestamp}",
    ]

start_datetime_str=date_list[0]
#for start_datetime_str in date_list:

start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S")
start_timestamp = start_datetime.timestamp()

print("timestamp initial")
print(formatted_timestamp)
print("start_timestamp", start_datetime)
end_datetime = start_datetime + timedelta(minutes= parameters['DURATION'])

end_timestamp = end_datetime.timestamp()
print("end_timestamp", end_datetime)
new_timestampManual = start_timestamp
target_timeManual = end_timestamp

all_services = query_svc_names("default",new_timestampManual, target_timeManual);

pod_names  = [(svc["pod"]) for svc in all_services]
#services_names = ['-'.join(svc["pod"].split('-')[:-2]) for svc in all_services]

print("les services")
#print(all_services)
print(pod_names)
#print(services_names)


for section_name in config.sections():
    directory = ""
    for key, value in config.items(section_name):
        directory = path_to_save(dir_name) + "/" + key

        for svc in pod_names:

            container_name = svc

            query_str = _init_metric_metadata(value, container_name)

            #payload = {'query': query_str, 'start': new_timestamp, 'end': current_timestamp, 'step': step}
            payload = {'query': query_str, 'start': new_timestampManual, 'end': target_timeManual, 'step': step}
            print("payload")
            print(payload)
            url = prom_url + '/api/v1/query_range?'

            res = None

            filename = svc + '.json'
            query_str_file = os.path.join(directory, filename)
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

    print("les donnes")
    print(query_str2)

    url = prom_url + '/api/v1/query_range?'

    payload = {'query': query_str, 'start': new_timestampManual, 'end': target_timeManual, 'step': step}
    payload2 = {'query': query_str2, 'start': new_timestampManual, 'end': target_timeManual, 'step': step}
    payload3 = {'query': query_str3, 'start': new_timestampManual, 'end': target_timeManual, 'step': step}
    payload4 = {'query': query_str4, 'start': new_timestampManual, 'end': target_timeManual, 'step': step}

    res = None

    directory2 = path_to_save(dir_name) + "/pod_info"
    directory3 = path_to_save(dir_name) + "/aggregation"

    print("url pour save")
    print(directory3)

    filename = container_name + '.json'
    filename2 = 'aggregation.json'
    filename3 = 'aggregation_memory.json'
    filename4 = 'pod_restart.json'

    query_str_file = os.path.join(directory2, filename)
    query_str_file2 = os.path.join(directory3, filename2)
    query_str_file3 = os.path.join(directory3, filename3)
    query_str_file4 = os.path.join(directory3, filename4)
    # query_str_file = "nom_du_fichier.json"
    os.makedirs(directory2, exist_ok=True)
    os.makedirs(directory3, exist_ok=True)
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

