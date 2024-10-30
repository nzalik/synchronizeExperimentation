import json
import os
import re
from datetime import date

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

cpu_step = "2m"

plot_limit = 301  # Replace with your preferred plot limit value

file_path_json = '../teastore.json'

def smooth(values, w_size=5):
    new_values = []
    for i in range(len(values)):
        window = values[max(0, i - (w_size - 1) // 2):min(i + w_size // 2 + 1, len(values))]
        new_values.append(sum(window) / len(window))
    return new_values

def get_color_for_serviceInit(service_name):
    service_name = service_name.lower()

    # Switch case avec 7 cas différents
    match service_name:
        case 'teastore-webui':
            return '#8ECAE6'
        case 'teastore-persistence':
            return '#219EBC'
        case 'teastore-db':
            return '#126782'
        case 'teastore-registry':
            return '#023047'
        case 'teastore-auth':
            return '#FFB703'
        case 'teastore-image':
            return '#FD9E02'
        case 'teastore-recommender':
            return '#FB8500'
        case _:
            return 'black'

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

def open_file(file_name):
    with open(file_name, 'r') as file:
        #for file_name in files:
        #with open(file_name, 'r') as file:
        json_data = json.load(file)
        return json_data

def plot_json(file_path, file_name):
    label = file_name
    list_element = os.listdir(file_path)


    json_data_file1 = open_file(os.path.join(file_path, list_element[0]))
    json_data_file2 = open_file(os.path.join(file_path, list_element[1]))
    json_data_file3 = open_file(os.path.join(file_path, list_element[2]))

    # json_data_file1 = open_file(os.path.join(directory,file_name, listElement[0]))
    # json_data_file2 = open_file(os.path.join(directory, file_name, listElement[1]))
    # json_data_file3 = open_file(os.path.join(directory, file_name, listElement[2]))

    if len(json_data_file1['data']['result']) > 0 and len(json_data_file2['data']['result']) > 0 and len(
            json_data_file3['data']['result']) > 0:
        datas1 = json_data_file1['data']['result'][0]['values']
        datas2 = json_data_file2['data']['result'][0]['values']
        datas3 = json_data_file3['data']['result'][0]['values']

        data_lengths = [len(datas1), len(datas2), len(datas3)]
        avg_length = sum(data_lengths) / len(data_lengths)

        if avg_length >= plot_limit:
            timestamps = np.array([int(ts) for ts, _ in datas1])

            given_value = 0.0  # Replace with your desired value
            # given_value = 1716985520.148 # Replace with your desired value

            greater_than_value = timestamps[timestamps > given_value]
            less_than_value = timestamps[timestamps <= given_value]

            values1 = [float(value) for _, value in datas1]
            values2 = [float(value) for _, value in datas2]
            values3 = [float(value) for _, value in datas3]

            longueur_max = max(len(liste) for liste in [values1, values2, values3])

            print(f"taille liste longue  {longueur_max}")
            print(len(values1))
            print(len(values2))
            print(len(values3))
            print("afterwards")
            for liste in [values1, values2, values3]:
                while len(liste) < longueur_max:
                    liste.append(0)

            values1 = np.array(values1)
            values2 = np.array(values2)
            values3 = np.array(values3)

            print(len(values1))
            print(len(values2))
            print(len(values3))

            meanValues = np.mean([values1, values2, values3], axis=0)

            last_ten_values = meanValues[-(len(greater_than_value)):]

            greater_than_valueReduce = greater_than_value

            new_timestamps = np.arange(0, plot_limit)

            last_ten_valuesReduce = last_ten_values

            # lissageValues = smooth(last_ten_valuesReduce)
            lissageValues = last_ten_valuesReduce

            # color = get_color_for_service(label)
            color = get_color_for_serviceInit(label)

            current_line = plt.plot([], [], color=color, label="")[0]
            legend_objectsCpu.append(current_line)
            legend_labelsCpu.append(label)

            plt.plot(new_timestamps, lissageValues, color=color, label=label)
            return new_timestamps, lissageValues
    return []

def plot_jsonMemory(file_path, file_name):
    label = file_name
    list_element = os.listdir(file_path)

    json_data_file1 = open_file(os.path.join(file_path, list_element[0]))
    json_data_file2 = open_file(os.path.join(file_path, list_element[1]))
    json_data_file3 = open_file(os.path.join(file_path, list_element[2]))

    # json_data_file1 = open_file(filesMem[0])
    # json_data_file2 = open_file(filesMem[1])
    # json_data_file3 = open_file(filesMem[2])

    if len(json_data_file1['data']['result']) > 0:
        datas1 = json_data_file1['data']['result'][0]['values']
        datas2 = json_data_file2['data']['result'][0]['values']
        datas3 = json_data_file3['data']['result'][0]['values']

        timestamps = np.array([int(ts) for ts, _ in datas1])

        given_value = 0.0  # Replace with your desired value
        # given_value = 1716985520.148 # Replace with your desired value

        greater_than_value = timestamps[timestamps > given_value]
        less_than_value = timestamps[timestamps <= given_value]

        values1 = [float(value) for _, value in datas1]
        values2 = [float(value) for _, value in datas2]
        values3 = [float(value) for _, value in datas3]

        print("avant avant")
        print(len(values1))
        print(len(values2))
        print(len(values3))
        longueur_max = max(len(liste) for liste in [values1, values2, values3])
        for liste in [values1, values2, values3]:
            while len(liste) < longueur_max:
                liste.append(0)

        values1 = np.array(values1)
        values2 = np.array(values2)
        values3 = np.array(values3)

        print("Après après 33333333333333333333333333")
        print(len(values1))
        print(len(values2))
        print(len(values3))

        meanValues = np.mean([values1, values2, values3], axis=0)

        # Normaliser les valeurs en gibibytes (GiB)
        normalized_values = []
        for value in meanValues:
            value_in_bytes = value  # Convertir en octets
            value_in_gib = value_in_bytes / (1000 ** 3)  # Convertir en GiB
            normalized_values.append(value_in_gib)  # Arrondir à 2 décimales
            # normalized_values.append(round(value_in_gib, 2))  # Arrondir à 2 décimales

        last_ten_values = normalized_values[-(len(greater_than_value)):]

        greater_than_valueReduce = greater_than_value
        last_ten_valuesReduce = last_ten_values

        new_timestamps = np.arange(0, plot_limit)

        # lissageValues = smooth(last_ten_valuesReduce)
        lissageValues = last_ten_valuesReduce

        #color, base_name = get_color_for_service(label)
        color = get_color_for_serviceInit(label)

        current_line = plt.plot([], [], color=color, label="")[0]
        legend_objectsMemory.append(current_line)
        legend_labelsMemory.append(label)

        plt.plot(new_timestamps, lissageValues, color=color, label=label)

        return new_timestamps
    return []

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

elts = ["linear_100"]
#elts = ["rd_stairs_2","rd_jump_2","li_stairsu_2","li_stairsd_2","linear_100"]
#elts = ["si_sin_2","si_cos_2","si_abssin_2","rd_stairs_2","rd_jump_2","li_stairsu_2","li_stairsd_2"]
#elts = [180, 200, 250, 300, 350]
#x = 1
cpu_limit_max=1.2
load_max=475
memory_limit=5
pod_limit=2


for x in elts:

    fileToPlot = f"output_{x}"
    #fileToPlot = f"output-linear_{x}requests_max_per_sec.csv"
    #fileToPlot = f"output-linear_80requests_max_per_sec.csv"
    save_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/variation/3replicas/nantes/hyperthreading/128/linear/3nodes/linear/29-10-2024/{x}/"
    #save_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/advanced/nantes/hyperthreading/128/linear/3nodes/linear/mean_calculation/{x}/"
    #save_path = f"../nantes/hyperthreading/16-07-2024/data/metrics/experimentation-output-linear_80requests_max_per_sec.csv/"

    #save_graphics_at = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/advanced/nantes/hyperthreading/128/linear/3nodes/linear/mean_calculation/{x}/Plots"
    save_graphics_at = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/variation/3replicas/nantes/hyperthreading/128/linear/3nodes/linear/29-10-2024/{x}/Plots"

    parameters = read_parameters_from_json(file_path_json)

    #cpu_step = parameters['CPU_STEP']

    plot_window = 150  # Show by interval of 5 minutes

    # Initialize the plot
    plt.figure(figsize=(10, 16))

    # Plot the first set of data
    plt.subplot(3, 1, 1)
    all_timestamps = []
    all_values = []

    today = date.today()
    dir_name = today.strftime("%d-%m-%Y")

    #save_graphics_at = f"../Plots/{dir_name}"  #TFB8500
    #save_graphics_at = f"../Plots"  #TFB8500
    # he directory where you want things to be saved
    if not os.path.exists(save_graphics_at):
        os.makedirs(save_graphics_at)

    legend_objectsCpu = []
    legend_labelsCpu = []

    directoryS = save_path + 'cpu/'

    listElement = os.listdir(directoryS)

    for element in listElement:
        directory = save_path + f"cpu/{element}/"
        #for file_name in os.listdir(directory):
        file_path = os.path.join(directory, element)
        #for file_name in json_files1:
        file_parts = file_path.split("/")
        last_part = (file_parts[-1]).split(".")[0]
        result = re.split(r'-\d+', last_part)[0]
        timestamps, values = plot_json(directory, element)

        if len(timestamps) > 0:
            all_timestamps.append(timestamps)
            all_values.append(values)

    # Concatenate all timestamps
    all_timestamps = np.concatenate(all_timestamps)

    # Calculate the start and end times
    start_time = min(all_timestamps)
    end_time = max(all_timestamps)

    # Generate a list of ticks every plot_window seconds
    ticks = np.arange(start_time, end_time + 1, plot_window)

    # Set ticks on the x-axis
    ticks_seconds = [((ts - start_time) // plot_window) * plot_window for ts in ticks]

    plt.axhline(y=1, color='r', linestyle='--')
    plt.xticks(ticks, ticks_seconds)
    plt.xlabel('Time (seconds)')
    plt.ylabel('cores per second')
    plt.title('CPU usage')
    plt.ylim(0, cpu_limit_max)
    #plt.grid(True)
    plt.xticks(rotation=45)

    # Séparer les objets et les labels après le tri
    legend_objects_sorted2, legend_labels_sorted2 = sort_legend(legend_objectsCpu, legend_labelsCpu)

    plt.legend(legend_objects_sorted2, legend_labels_sorted2)

    #plt.legend()

    # Plot the second set of data
    plt.subplot(3, 1, 2)
    all_timestamps2 = []

    legend_objectsMemory = []
    legend_labelsMemory = []

    directoryS2 = save_path + 'memory/'

    listElement = os.listdir(directoryS2)

    for element in listElement:
        directory2 = save_path + f"memory/{element}/"
        file_path = os.path.join(directory2, element)
        print("lr chemon")
        print(file_path)
        #for file_name in json_files1:
        file_parts = file_path.split("/")
        last_part = (file_parts[-1]).split(".")[0]
        result = re.split(r'-\d+', last_part)[0]
        timestamps2 = plot_jsonMemory(directory2, last_part)

        if len(timestamps2) > 0:
            all_timestamps2.append(timestamps2)


    # Concatenate all timestamps
    all_timestamps2 = np.concatenate(all_timestamps2)

    # Calculate the start and end times
    start_time2 = min(all_timestamps2)
    end_time2 = max(all_timestamps2)

    # Generate a list of ticks every 20 seconds
    ticks2 = np.arange(start_time2, end_time2 + plot_window, plot_window)

    # Set ticks on the x-axis
    ticks_seconds2 = [((ts - start_time2) // plot_window) * plot_window for ts in ticks2]


    plt.xticks(ticks2, ticks_seconds2)

    plt.xlabel('Time (seconds)')
    plt.ylabel('Memory (Gbytes)')
    plt.title('Memory usage')
    plt.ylim(0, memory_limit)
    #plt.grid(True)
    plt.xticks(rotation=45)

    # Séparer les objets et les labels après le tri
    legend_objects_sorted, legend_labels_sorted = sort_legend(legend_objectsMemory, legend_labelsMemory)

    plt.legend(legend_objects_sorted, legend_labels_sorted)

    lastEl = ticks_seconds2[-1]

    plt.subplot(3, 1, 3)

    all_timestamps3 = []
    # Read JSON data from a file
    directory3 = save_path + 'pod_info/pod_info.json'

    with open(directory3, 'r') as file:
        source = json.load(file)

    timestamps = []
    values = []
    all_timestamps = []

    data_list = source['data']['result']

    legend_objects = []
    legend_labels = []

    for json_data in data_list:
        # Convertir la chaîne JSON en un dictionnaire Python
        result = json_data

        # Extraire les valeurs et les timestamps
        timestamps = [int(x[0]) for x in result["values"]]
        values = [int(x[1]) for x in result["values"]]

        all_timestamps.append(timestamps)

        # Récupérer le nom de la métrique et du déploiement
        metric_name = result["metric"]["__name__"]
        deployment_name = result["metric"]["deployment"]

        line = plt.plot([], [], color=get_color_for_serviceInit(deployment_name), label="")[0]
        legend_objects.append(line)
        legend_labels.append(deployment_name)
        # plt.plot(timestamps, values, color=get_color_for_serviceInit(deployment_name), label=f"{deployment_name}")

        color = get_color_for_serviceInit(deployment_name)
        # Tracer la courbe
        plt.plot(timestamps, values, color=color, label=f"{deployment_name}")

    all_timestamps = np.concatenate(all_timestamps)

    start_time4 = min(timestamps)
    end_time4 = max(timestamps)

    ticks4 = np.arange(start_time4, end_time4 + 1, plot_window)

    ticks_seconds4 = [((ts - start_time4) // plot_window) * plot_window for ts in ticks4]
    plt.ylim(0, pod_limit)
    plt.xticks(ticks4, ticks_seconds4)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Number of pods')
    plt.title('Evolution of pods')

    plt.xticks(rotation=45)

    plt.legend(legend_objects, legend_labels, loc='upper center', ncol=2)

    plt.tight_layout()

    files = os.listdir(save_graphics_at)
    data_count = sum(1 for f in files if f.startswith("output") and f.endswith(".png"))
    my_string = f"{save_graphics_at}/output{str(data_count + 1)}-{x}.png"
    print(my_string)
    #plt.savefig(my_string)
    plt.show()
