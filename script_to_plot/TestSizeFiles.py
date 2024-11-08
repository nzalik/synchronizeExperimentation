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


def plot_json_generic(file_path, file_name, data_type='cpu'):
    """
    :param file_path: str - The path to the directory containing JSON files.
    :param file_name: str - The name of the file to be labeled in the plot.
    :param data_type: str - The type of data to be processed, default is 'cpu'.
    :return: np.ndarray - Array of new timestamps generated for plotting.
    """
    is_cpu = data_type == 'cpu'
    label = file_name
    list_element = os.listdir(file_path)

    json_data_files = [open_file(os.path.join(file_path, file)) for file in list_element]

    for i, json_data_file in enumerate(json_data_files, 1):
        print(f"json_data_file{i}", json_data_file)

    if all('data' in json_data_file and 'result' in json_data_file['data'] and len(json_data_file['data']['result']) > 0
           for json_data_file in json_data_files):
        datas_list = [json_data_file['data']['result'][0]['values'] for json_data_file in json_data_files]

        selected_values = []

        for values in datas_list:
            if len(values) > plot_limit:
                selected_values = values
                break

        timestamps = np.array([int(ts) for ts, _ in selected_values])
        given_value = 0.0

        greater_than_value = timestamps[timestamps > given_value]

        values_list = [[float(value) for _, value in datas] for datas in datas_list]

        print("###########les valeurs#######################")
        for values in values_list:
            #print(values)
            print(len(values))

        print("******************completion*************************")
        longueur_max = plot_limit

        # for values in values_list:
        #     if len(values) > longueur_max:
        #         del values[:-longueur_max]
        #     else:
        #         while len(values) < longueur_max:
        #             values.append(0)

        values_arrays = [np.array(values) for values in values_list]
        meanValues = np.mean(values_arrays, axis=0)

        if not is_cpu:
            normalized_values = [value / (1000 ** 3) for value in meanValues]
            last_ten_values = normalized_values[-(len(greater_than_value)):]
        else:
            last_ten_values = meanValues[-(len(greater_than_value)):]

        new_timestamps = np.arange(0, plot_limit)
        lissageValues = last_ten_values

        color = get_color_for_serviceInit(label)

        current_line = plt.plot([], [], color=color, label="")[0]
        if is_cpu:
            legend_objectsCpu.append(current_line)
            legend_labelsCpu.append(label)
        else:
            legend_objectsMemory.append(current_line)
            legend_labelsMemory.append(label)

        #plt.plot(new_timestamps, lissageValues, color=color, label=label)
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

#elts = ["si_sin_2"]
elts = ["linear_100"]
#elts = ["si_sin_2","si_cos_2","si_abssin_2","rd_stairs_2","rd_jump_2","li_stairsu_2","li_stairsd_2"]
#elts = [180, 200, 250, 300, 350]
#x = 1
cpu_limit_max=1.2
load_max=475
memory_limit=5
pod_limit=2


for x in elts:
    print(x)
    fileToPlot = f"output_{x}"
    #fileToPlot = f"output-linear_{x}requests_max_per_sec.csv"
    #fileToPlot = f"output-linear_80requests_max_per_sec.csv"
    save_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/organised/nantes/hyperthreading/128/linear/3nodes/linear/28-10-2024/{x}/"
    #save_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/advanced/nantes/hyperthreading/128/linear/3nodes/linear/mean_calculation/{x}/"
    #save_path = f"../nantes/hyperthreading/16-07-2024/data/metrics/experimentation-output-linear_80requests_max_per_sec.csv/"

    #save_graphics_at = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/advanced/nantes/hyperthreading/128/linear/3nodes/linear/mean_calculation/{x}/Plots"
    save_graphics_at = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/organised/nantes/hyperthreading/128/linear/3nodes/linear/28-10-2024/{x}/Plots"

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

    legend_objectsMemory = []
    legend_labelsMemory = []
    
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
        timestamps = plot_json_generic(directory, element, data_type='cpu')

        if len(timestamps) > 0:
            all_timestamps.append(timestamps)
            #all_values.append(values)

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


    plt.tight_layout()

    files = os.listdir(save_graphics_at)
    data_count = sum(1 for f in files if f.startswith("output") and f.endswith(".png"))
    my_string = f"{save_graphics_at}/output{str(data_count + 1)}-{x}.png"
    print(my_string)
    #plt.savefig(my_string)
    #plt.show()
