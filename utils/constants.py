import configparser
import json
import os
from datetime import datetime
import requests
import numpy as np
import matplotlib.pyplot as plt
line_styles=["solid","dotted","dashed","dashdot"]

plot_limit = 298
cpu_limit_max=0.002
load_max=11
memory_limit=0.01
pod_limit=2
request_volume_limit = 11

range_limit=2
harmonization=False

colors_table = [
    "#FF5733",  # Rouge orangé
    "#33FF57",  # Vert Lime
    "#3357FF",  # Bleu Foncé
    "#003049",  # Bleu profond
    "#F9C74F",  # Jaune doré
    "#8E44AD",  # Violet foncé
    "#E74C3C",  # Rouge vif
    "#1ABC9C",  # Turquoise
    "#FFC300",  # Jaune vif
    "#7D3C98"   # Violet profond
]

# def get_color_for_service_init(service_name):
#     service_name = service_name.lower()
#
#     # Switch case avec 7 cas différents
#     match service_name:
#         case 'teastore-webui':
#             return '#8ECAE6'
#         case 'teastore-persistence':
#             return '#eb014f'
#         case 'teastore-db':
#             return '#126782'
#         case 'teastore-registry':
#             return '#023047'
#         case 'teastore-auth':
#             return '#FFB703'
#         case 'teastore-image':
#             return '#067d4a'
#         case 'teastore-recommender':
#             return '#9c23c2'
#         case _:
#             return '#adb5bd'

#Match case is not usable before python version 3.12
def get_color_for_service_init(service_name):
    service_name = service_name.lower()

    if service_name == 'teastore-webui':
        return '#8ECAE6'
    elif service_name == 'teastore-persistence':
        return '#eb014f'
    elif service_name == 'teastore-db':
        return '#126782'
    elif service_name == 'teastore-registry':
        return '#023047'
    elif service_name == 'teastore-auth':
        return '#FFB703'
    elif service_name == 'teastore-image':
        return '#067d4a'
    elif service_name == 'teastore-recommender':
        return '#9c23c2'
    else:
        return '#adb5bd'

def normalization(value):
    return value / (1000 ** 3)

def get_color_for_service(service_name):
    service_name = service_name.lower()

    # Récupérer le nom de base du service (sans le numéro ni le hachage)
    base_name = '-'.join(service_name.split('-')[:-2])

    # Récupérer le numéro du service (s'il y en a un)
    try:
        instance_number = int(service_name.split('-')[-2])
    except ValueError:
        instance_number = 1

    # Définir les couleurs de base pour chaque service
    color_map = {
        'teastore-webui': '#8ECAE6',
        'teastore-persistence': '#219EBC',
        'teastore-db': '#126782',
        'teastore-registry': '#023047',
        'teastore-auth': '#FFB703',
        'teastore-image': '#FD9E02',
        'teastore-recommender': '#FB8500'
    }

    # Choisir la couleur en fonction du numéro d'instance
    base_color = color_map.get(base_name, 'black')
    if instance_number > 1:
        hue = (instance_number - 1) * 60  # Décalage de la teinte de 60 degrés par instance
        color = f'hsl({hue}, 100%, 50%)'
    else:
        color = base_color

    return color, base_name

def smooth(values, w_size=7):
    new_values = []
    for i in range(len(values)):
        window = values[max(0, i - (w_size - 1) // 2):min(i + w_size // 2 + 1, len(values))]
        new_values.append(sum(window) / len(window))
    return new_values


def open_file(file_name):
    with open(file_name, 'r') as file:
        #for file_name in files:
        #with open(file_name, 'r') as file:
        json_data = json.load(file)
        return json_data

def read_parameters_from_json(file_path):
    with open(file_path, 'r') as file:
        parameters = json.load(file)
    return parameters

def sort_legend(legend_objects, legend_labels):
    """
    Trie les objets de légende et leurs labels par ordre alphabétique.

    Parameters:
    - legend_objects: Liste des objets de légende.
    - legend_labels: Liste des labels de légende.

    Returns:
    - Objects et labels triés.
    """
    # Créer des paires d'objets et de labels
    legend_pairs = list(zip(legend_objects, legend_labels))

    # Trier les paires par labels
    legend_pairs_sorted = sorted(legend_pairs, key=lambda x: x[1])

    # Séparer les objets et les labels après le tri
    legend_objects_sorted, legend_labels_sorted = zip(*legend_pairs_sorted)

    return legend_objects_sorted, legend_labels_sorted

cpu_step = "120s"
step = "1s"

def read_ini_file(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def path_to_save(init_path):
    #output_path = f"{init_path}/experimentation-{string_argument}"
    output_path = f"{init_path}"
    if os.path.exists(init_path):
        # Construire le nouveau nom de répertoire
        new_dir_name = f"data_{datetime.now().strftime('%H')}"
        #output_path = f"{init_path}/experimentation-{string_argument}"
        output_path = f"{init_path}"

        if not os.path.exists(init_path):
            os.makedirs(init_path)

    return output_path

def query_prometheus(query, prom_url):
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

def query_svc_names(namespace='default', start_dt="", end_dt="", prom_url=""):
    #query_str = 'label/pod/values?match[]=kube_pod_container_info{namespace="' + namespace + '"}'
    query_str = 'label/pod/values?match[]=kube_pod_container_info{namespace="' + namespace + '"}&start=' + str(
        start_dt) + '&end=' + str(end_dt)
    res = query_prometheus(query_str, prom_url)
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

def init_metric_metadata(metric, pod_name, prom_url):

    query_str = 'metadata?metric=' + metric
    url = prom_url + '/api/v1/' + query_str

    res = None

    root_container_name = '-'.join(pod_name.split('-')[:-2])

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
            return f"rate({metric}{{namespace=\"default\",pod=\"{pod_name}\", container=\"{root_container_name}\"}}[{cpu_step}])"
        else:
            return f"{metric}{{namespace=\"default\"}}"


def plot_json_generic(file_path, file_name, data_type='cpu'):
    is_cpu = data_type == 'cpu'
    label = file_name
    print(data_type)
    list_element = sorted(os.listdir(file_path))
    print(list_element)

    #print(list_element[0])
    json_data_file1 = open_file(os.path.join(file_path, list_element[0]))
    #print(list_element[1])
    json_data_file2 = open_file(os.path.join(file_path, list_element[1]))
    #print(list_element[2])
    json_data_file3 = open_file(os.path.join(file_path, list_element[2]))
    # json_data_file4 = open_file(os.path.join(file_path, list_element[3]))
    # json_data_file5 = open_file(os.path.join(file_path, list_element[4]))
    # json_data_file6 = open_file(os.path.join(file_path, list_element[5]))
    # json_data_file7 = open_file(os.path.join(file_path, list_element[6]))
    #json_data_file8 = open_file(os.path.join(file_path, list_element[7]))
    #
    # print(json_data_file1)
    # print(json_data_file2)
    # print(json_data_file3)
    #print(json_data_file4)

    if len(json_data_file1['data']['result']) > 0 :
        datas1 = json_data_file1['data']['result'][0]['values']
        datas2 = json_data_file2['data']['result'][0]['values']
        datas3 = json_data_file3['data']['result'][0]['values']
        # datas4 = json_data_file4['data']['result'][0]['values']
        # datas5 = json_data_file5['data']['result'][0]['values']
        # datas6 = json_data_file6['data']['result'][0]['values']
        # datas7 = json_data_file7['data']['result'][0]['values']
        #datas8 = json_data_file8['data']['result'][0]['values']


        selected_values=[]

        valid_values_list = [datas1, datas2]
        for values in valid_values_list:
            if len(values) > plot_limit:
                selected_values = values
                break
        #timestamps = np.array([int(ts) for ts, _ in datas1])
        timestamps = np.array([int(ts) for ts, _ in selected_values])
        given_value = 0.0

        greater_than_value = timestamps[timestamps > given_value]

        values1 = [float(value) for _, value in datas1]
        values2 = [float(value) for _, value in datas2]
        values3 = [float(value) for _, value in datas3]
        # values4 = [float(value) for _, value in datas4]
        # values5 = [float(value) for _, value in datas5]
        # values6 = [float(value) for _, value in datas6]
        # values7 = [float(value) for _, value in datas7]
#        values8 = [float(value) for _, value in datas8]

        # print("###########les valeurs#######################")
        # print(values1)
        # print(values2)
        # print(values3)
        #print(values4)

        longueur_max = plot_limit
        # longueur_max = max(len(liste) for liste in [values1, values2, values3])
        for liste in [values1, values2]:
            if len(liste) > longueur_max:
                # Couper pour garder les longueur_max derniers éléments
                del liste[:-longueur_max]
            else:
                while len(liste) < longueur_max:
                 liste.append(0)


        values1 = np.array(smooth(values1))
        values2 = np.array(smooth(values2))
        values3 = np.array(smooth(values3))
        # values4 = np.array(smooth(values4))
        # values5 = np.array(smooth(values5))
        # values6 = np.array(smooth(values6))
        # values7 = np.array(smooth(values7))
        #values8 = np.array(smooth(values8))

        # print(len(values1))
        # print(len(values2))
        # print(len(values3))
        #print(len(values4))
        #print(len(values5))

        meanValues = np.mean([values1, values2], axis=0)

        if not is_cpu:
            normalized_values = [value / (1000 ** 3) for value in meanValues]
            last_ten_values = normalized_values[-(len(greater_than_value)):]
        else:
            last_ten_values = meanValues[-(len(greater_than_value)):]

        new_timestamps = np.arange(0, plot_limit)
        lissageValues = last_ten_values

        #color = get_color_for_service_init(label)


        current_line = plt.plot([], [], label="")[0]

        # if is_cpu:
        #     legend_objectsCpu.append(current_line)
        #     legend_labelsCpu.append(label)
        # else:
        #     legend_objectsMemory.append(current_line)
        #     legend_labelsMemory.append(label)

        #temp_list = [values1, values2]
        temp_list = [values1, values2, values3][:range_limit]
        for index, tab in enumerate(temp_list):
            print(index)
            #tab = temp_list[i-1]
            if is_cpu:
                plt.plot(new_timestamps, tab, color = colors_table[index], label=label+str(index+1), linestyle=line_styles[index % len(line_styles)])
            else:
                plt.plot(new_timestamps, normalization(tab), color = colors_table[index], label=label+str(index+1), linestyle=line_styles[index % len(line_styles)])

        #plt.plot(new_timestamps, lissageValues, color=color, label=label)
        return new_timestamps, current_line, label
        #return new_timestamps, lissageValues if is_cpu else new_timestamps
    return []

def plot_metrics(data, elt, position, metric_to_plot=""):
    global timestamps
    results = data['data']['result']

    for result in results:
        metric = result['metric']
        source_workload = metric.get('source_workload', 'unknown')
        destination = metric.get('destination_workload', elt)

        source_workload_txt = source_workload
        #source_workload_txt = source_workload.split('-')[1] if '-' in source_workload else source_workload
        destination_txt = destination
        #destination_txt = destination.split('-')[1]

        timestamps = np.arange(0, plot_limit)  # Adjust the step value as needed for your specific interval

        valuesInit = [0 if point[1] == "NaN" else float(point[1]) for point in
                      result['values'][:plot_limit]] + [0] * (
                             plot_limit - min(plot_limit, len(
                         result['values'])))  # Remplacer NaN par 0 et compléter avec des 0 si nécessaire

        multiplier_note = ''
        if harmonization and metric_to_plot == "latency":
            if destination != 'teastore-webui' and metric_to_plot == "latency":
                valuesInit = [x * 5 for x in valuesInit]  # Multiply values by a factor for non-webui destinations
                multiplier_note = ' (x5)'
            else:
                multiplier_note = ''


        values = smooth(valuesInit)
        heures = [datetime.fromtimestamp(ts).strftime('%M') for ts in timestamps]

        #color = get_color_for_service_init(source_workload)
        color = colors_table[position]
        if metric_to_plot == "latency":
            plt.plot(timestamps, values, color=color,
                    #label=f'{destination_txt + str(position + 1)}{multiplier_note}',
                    #label=f'{source_workload_txt + str(position + 1)}{multiplier_note}',
                    label=f'{destination_txt + str(position + 1)}{multiplier_note}',
                     linestyle=line_styles[position % len(line_styles)])
        else:
            plt.plot(timestamps, values, color=color,
                     label=f'{destination_txt + str(position + 1)}{multiplier_note}',
                     # label=f'{source_workload_txt + str(position + 1)} → {destination_txt + str(position + 1)}{multiplier_note}',
                     linestyle=line_styles[position % len(line_styles)], marker='o', ms=4)


    # start_time = min(timestamps)
    # end_time = max(timestamps)
    #
    # ticks = np.arange(start_time, end_time + 1, plot_window)
    # ticks_seconds = [((ts - start_time) // plot_window) * plot_window for ts in ticks]
    # plt.set_xticks(ticks)
    # plt.set_xticklabels(ticks_seconds)
    #
    # plt.set_xlabel('Time (seconds)')
    # plt.set_ylabel('rps (requests per second)')
    # plt.set_title(f'Request volume')
    # #plt.set_title(f'Requests volume send to {elt}')
    # if metric_to_plot=="latency":
    #     plt.set_ylabel('Latency (ms)')
    #     plt.set_title(f'Request duration')
    #     #plt.set_title(f'Request duration to {elt}')
    #
    # plt.set_ylim(0, max_value)


    return []
