import os
import requests
from datetime import datetime, timedelta
import json
import sys

def read_parameters_from_json(file_path):
    with open(file_path, 'r') as file:
        parameters = json.load(file)
    return parameters

file_path = '../teastore_grenoble.json'
metric_path="../istio_metrics.json"

complete_storage_dir = ""
formattedDate=""

if len(sys.argv) > 1:
    complete_storage_dir = sys.argv[1]
    formattedDate = sys.argv[2]

parameters = read_parameters_from_json(file_path)

metrics_parameters = read_parameters_from_json(metric_path)

prometheus_url = parameters['PROMETHEUS_URL']

current_date = datetime.now().strftime('%Y-%m-%d')


start_datetime_str=  current_date +" "+ formattedDate


start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S.%f")
end_datetime = start_datetime + timedelta(minutes=parameters['DURATION'])

start_dt = start_datetime.timestamp()
end_dt = end_datetime.timestamp()

namespace="default"
time_step="1"
step="1"

dir_name = f"{complete_storage_dir}/data/metrics/latency"

if not os.path.exists(dir_name):
    os.makedirs(dir_name)

def query_prometheus(prometheus_url, query, start_dt, end_dt, step):
    payload = {'query': query, 'start': start_dt, 'end': end_dt, 'step': step + 's'}

    url = prometheus_url + '/api/v1/' + query
    print("Querying " + url)
    res = None

    try:
        res = requests.get(url).json()
    except Exception as e:
        print(e)
        print("...Fail at Prometheus.")

    if res != None and 'error' in res:
        print(res["error"])
        res = None

    return res


def query_prometheus_with_payload(prometheus_url, query, start_dt, end_dt, step):
    #payload = {'query': query, 'start': start_dt, 'end': end_dt, 'step': step + 's'}
    payload = {'query': query, 'start': start_dt, 'end': end_dt, 'step': step + 's'}

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

def query_svc_names(prometheus_url, namespace='default', start_dt='', end_dt='', step='1'):
    query_str = '/label/pod/values?match[]=kube_pod_container_info{namespace="' + namespace + '"}&start=' + str(
        start_dt) + '&end=' + str(end_dt)
    print("Querying existing services by " + query_str)
    res = query_prometheus(prometheus_url, query_str, start_dt, end_dt, step)
    svc_names = []
    services = []
    if res != None:
        svc_names = res['data']
        for name in svc_names:
            # query_str = '/query?query=container_last_seen{namespace="' + namespace + '", pod="' + name + '"}'
            query_str = 'container_last_seen{namespace="' + namespace + '", pod="' + name + '"}'
            res = query_prometheus_with_payload(prometheus_url, query_str, start_dt, end_dt, step)
            if res != None and len(res['data']['result']) > 0:
                instance = res['data']['result'][0]['metric']['instance'].split(':')[0]
                # node = res['data']['result'][0]['metric']['node']
                service_obj = {'pod': name, 'instance': instance}
                services.append(service_obj)

    return services


def query_for_service(self, prometheus_url, svc, start_dt, end_dt, step, datadir, second_svc):
    query_str = self._query_str(svc, second_svc)
    payload = {'query': query_str, 'start': start_dt.timestamp(), 'end': end_dt.timestamp(), 'step': step + 's'}

    url = prometheus_url + '/api/v1/query_range?'
    print("Querying " + url + " with payload " + str(payload))
    res = None

    # Query Prometheus
    try:
        res = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload).json()
    except Exception as e:
        print(e)
        print("...Fail at Prometheus request.")

    if res != None and 'error' in res:
        print("ERROR ", res["error"])
        res = None

    elif res != None and len(res['data']['result']) > 0:
        print("...saving data.")
        self._save_as_json(res, datadir, second_svc)

    return res

def _query_str(self, svc, dst_app="teastore", code="200", reporter="destination", job="kubernetes-pods"):
    if "gen" in svc['pod']:
        svc_name = svc['pod'].split("-")[0]
        return self.query_modifier(
            self.name + '{request_protocol="http", destination_app="' + dst_app + '", destination_workload="teastore-webui", reporter="source", job="' + job + '", source_app="gens", source_workload="' + svc_name + '"}')

    svc_name = "-".join(svc['pod'].split("-")[:2])
    return self.query_modifier(
        self.name + '{request_protocol="http", destination_service="' + svc_name + '.default.svc.cluster.local", destination_app="' + dst_app + '", destination_workload="' + svc_name + '", reporter="destination", job="' + job + '", source_app="gens", source_workload="gen"}')


def _save_as_json(source, destination, res, datadir):
    # Sauvegarder les métriques dans un fichier
    print("Sauvegarde des données pour", source, "vers", destination)

    # Créer le chemin du fichier avec le nom du service source et destination
    filename = f"latencies_to_{destination}.json"
    filepath = os.path.join(datadir, filename)

    # Créer le répertoire s'il n'existe pas
    os.makedirs(datadir, exist_ok=True)

    # Sauvegarder les données au format JSON
    with open(filepath, 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)

    print(f"Données sauvegardées dans {filepath}")


services = query_svc_names(prometheus_url, namespace=namespace, start_dt=start_dt, end_dt=end_dt, step=time_step)

services_names = ['-'.join(svc["pod"].split('-')[:-2]) for svc in services]


#for source_workload in services:
for destination_workload in services:
   # source = '-'.join(source_workload["pod"].split('-')[:-2])  # Adapter selon ta structure de données
    destination = '-'.join(destination_workload["pod"].split('-')[:-2])

    # query_str = f"""
    # histogram_quantile(0.95, sum(rate(istio_request_duration_milliseconds_bucket{{reporter="source",destination_workload="{destination}", source_workload="{source}"}}[30s])) by (le, destination_workload))
    # """
    query_str = f"""

    """
    payload = {'query': query_str, 'start': start_dt, 'end': end_dt, 'step': step + 's'}

    url = prometheus_url + '/api/v1/query_range?'
    res = None

    try:
        res = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload).json()
    except Exception as e:
        print(e)
        print("...Fail at Prometheus request.")

    if res != None and 'error' in res:
        print("ERROR ", res["error"])
        res = None

    elif res != None and len(res['data']['result']) > 0:
        print("...saving data.")
        _save_as_json(destination, destination, res, dir_name)
