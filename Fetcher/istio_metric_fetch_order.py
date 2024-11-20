import os
import requests
from datetime import datetime, timedelta
import json
import sys

from utils.constants import cpu_step


def read_parameters_from_json(file_path):
    with open(file_path, 'r') as file:
        parameters = json.load(file)
    return parameters

complete_storage_dir = ""
formattedDate=""

if len(sys.argv) > 1:
    complete_storage_dir = sys.argv[1]
    formattedDate = sys.argv[2]

# file_path = '../teastore_grenoble.json'
# metrics_path = '../istio_metrics.json'

#metrics_path = sys.argv[3]
prometheus_url = sys.argv[4]
duration = sys.argv[5]
profile = sys.argv[6]
exp_nb = sys.argv[7]

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
metrics_path = f"{parent_dir}/istio_metrics.json"

#parameters = read_parameters_from_json(file_path)

metric_parameters = read_parameters_from_json(metrics_path)

#prometheus_url = parameters['PROMETHEUS_URL']

current_date = datetime.now().strftime('%Y-%m-%d')

start_datetime_str=  current_date +" "+ formattedDate

start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S")
end_datetime = start_datetime + timedelta(minutes=int(duration))

start_dt = start_datetime.timestamp()
end_dt = end_datetime.timestamp()

namespace="default"
time_step="1"
step="1"
interval = cpu_step

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
    query_str = 'label/pod/values?match[]=kube_pod_container_info{namespace="' + namespace + '"}&start=' + str(
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


# def query_for_service(self, prometheus_url, svc, start_dt, end_dt, step, datadir, second_svc):
#     query_str = self._query_str(svc, second_svc)
#     payload = {'query': query_str, 'start': start_dt.timestamp(), 'end': end_dt.timestamp(), 'step': step + 's'}
# 
#     url = prometheus_url + '/api/v1/query_range?'
#     print("Querying " + url + " with payload " + str(payload))
#     res = None
# 
#     # Query Prometheus
#     try:
#         res = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload).json()
#     except Exception as e:
#         print(e)
#         print("...Fail at Prometheus request.")
# 
#     if res != None and 'error' in res:
#         print("ERROR ", res["error"])
#         res = None
# 
#     elif res != None and len(res['data']['result']) > 0:
#         print("...saving data.")
#         self._save_as_json(res, datadir, second_svc)
# 
#     return res

def _get_query_modifier(metric_parameter, destination_target):

    if metric_parameter['aggregator'] == "histogram_quantile":
        return f""" histogram_quantile(0.95, sum(rate(istio_request_duration_milliseconds_bucket{{reporter=~"destination", destination_workload="{destination_target}"}}[{interval}])) by (le, destination_workload))"""
    elif metric_parameter['aggregator'] == "round_aggr":
        return f""" round(sum(irate(istio_requests_total{{destination_workload="{destination_target}",reporter=~"destination"}}[{interval}])) by (destination_workload), 0.001)"""
    elif metric_parameter['aggregator'] == "round":
        return f""" round(sum(irate(istio_requests_total{{destination_workload="{destination_target}",reporter=~"destination"}}[{interval}])) by (destination_workload), 0.001)"""
    elif metric_parameter['aggregator'] == "request_success":
        return f""" round(sum(irate(istio_requests_total{{destination_workload="{destination_target}",reporter=~"destination", response_code=~"2.."}}[{interval}])) by (destination_workload), 0.001)"""
    elif metric_parameter['aggregator'] == "client_error":
        return f""" round(sum(irate(istio_requests_total{{destination_workload="{destination_target}",reporter=~"destination", response_code=~"4.."}}[{interval}])) by (destination_workload), 0.001)"""
    elif metric_parameter['aggregator'] == "server_error":
        return f""" round(sum(irate(istio_requests_total{{destination_workload="{destination_target}",reporter=~"destination", response_code=~"5.."}}[{interval}])) by (destination_workload), 0.001)"""
    elif metric_parameter['aggregator'] == "redirection":
        return f""" round(sum(irate(istio_requests_total{{destination_workload="{destination_target}",reporter=~"destination", response_code=~"3.."}}[{interval}])) by (destination_workload), 0.001)"""
    elif metric_parameter['aggregator'] == "bytes":
        return f"""histogram_quantile(0.95, sum(irate(istio_request_bytes_bucket{{reporter=~"destination", destination_workload=~"{destination_target}"}}[{interval}])) by (le, source_workload, destination_workload))"""
    elif metric_parameter['aggregator'] == "tcp":
        return f"""round(sum(irate(istio_tcp_sent_bytes_total{{reporter=~"destination", destination_workload=~"{destination_target}"}}[{interval}])) by (destination_workload), 0.001)"""
    elif metric_parameter['aggregator'] == "latency_order":
        return f"""topk(64, histogram_quantile(0.95, sum(rate(istio_request_duration_milliseconds_bucket{{namespace="default"}}[{interval}])) by (le, destination_workload)))"""
    else:
        return f""" round(sum(irate(istio_requests_total{{reporter=~"destination", destination_workload="{destination_target}", response_code="400"}}[{interval}])) by (destination_workload), 0.001)"""


def _save_as_json(source, destination, res, datadir):
    # Sauvegarder les métriques dans un fichier

    #root_container_name = '-'.join(svc.split('-')[:-2])

    dir_name = f"{complete_storage_dir}/{datadir}/{destination}/{profile}/"
    #profile = complete_storage_dir.split('/')[-1]

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # Créer le chemin du fichier avec le nom du service source et destination
    filename = f"{dir_name}{exp_nb}_{datadir}_to_{destination}_{profile}.json"
    filepath = os.path.join(datadir, filename)
    # if os.path.exists(filepath):
    #     base, ext = os.path.splitext(filename)
    #     counter = 1
    #     while os.path.exists(os.path.join(datadir, f"{base}_{counter}{ext}")):
    #         counter += 1
    #     filepath = os.path.join(datadir, f"{base}_{counter}{ext}")
    # Créer le répertoire s'il n'existe pas
    os.makedirs(datadir, exist_ok=True)

    # Sauvegarder les données au format JSON
    with open(filepath, 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)


services = query_svc_names(prometheus_url, namespace=namespace, start_dt=start_dt, end_dt=end_dt, step=time_step)

services_names = ['-'.join(svc["pod"].split('-')[:-2]) for svc in services]


for destination_workload in services:
    for metric in metric_parameters:
        print("on etst entré")
        dir_name = metric["name"]
       # source = '-'.join(source_workload["pod"].split('-')[:-2])  # Adapter selon ta structure de données
        destination = '-'.join(destination_workload["pod"].split('-')[:-2])

        # query_str = f"""
        # histogram_quantile(0.95, sum(rate(istio_request_duration_milliseconds_bucket{{reporter="source",destination_workload="{destination}", source_workload="{source}"}}[{interval}])) by (le, destination_workload))
        # """
        #query_str = _get_query_modifier(metric, destination)
        query_str = _get_query_modifier(metric, destination)

        payload = {'query': query_str, 'start': start_dt, 'end': end_dt, 'step': step + 's'}

        url = prometheus_url + '/api/v1/query_range?'
        res = None

        try:
            res = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload).json()
            print(res)
        except Exception as e:
            print(e)
            print("...Fail at Prometheus request.")

        if res != None and 'error' in res:
            print("ERROR ", res["error"])
            res = None

        elif res != None and len(res['data']['result']) > 0:
            print("...saving data.")
            _save_as_json(destination, destination, res, dir_name)
