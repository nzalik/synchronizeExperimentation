import json
import os
import re
from datetime import date

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

elts = [200, 250, 300, 350]
#x = 1
cpu_limit_max=1.2
load_max=475
memory_limit=5
pod_limit=6

#while x <= 1:
for x in elts:
    def read_parameters_from_json(file_path):
        with open(file_path, 'r') as file:
            parameters = json.load(file)
        return parameters


    plot_path = "../nantes/hyperthreading/128/group/3nodes/test2/after250/linear/10-08-2024/experimentation1/data/load/"

    #fileToPlot = f"linear_{x}requests_per_sec.csv"
    fileToPlot = f"output-linear_{x}requests_max_per_sec.csv"
    #fileToPlot = f"output-linear_80requests_max_per_sec.csv"

    cpu_step = "2m"

    file_path = '../teastore.json'

    save_path = f"../nantes/hyperthreading/128/group/3nodes/test2/after250/linear/10-08-2024/experimentation1/data/metrics/experimentation-output-linear_{x}requests_max_per_sec.csv/"
    #save_path = f"../nantes/hyperthreading/16-07-2024/data/metrics/experimentation-output-linear_80requests_max_per_sec.csv/"

    save_graphics_at = f"../nantes/hyperthreading/128/group/3nodes/test2/after250/linear/10-08-2024/experimentation1/data/Plots"

    parameters = read_parameters_from_json(file_path)

    #cpu_step = parameters['CPU_STEP']

    plot_window = 150  # Show by interval of 5 minutes


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

        return color


    def plot_json(file_name, label):
        with open(file_name, 'r') as file:
            json_data = json.load(file)

        if len(json_data['data']['result']) > 0:
            datas = json_data['data']['result'][0]['values']

            timestamps = np.array([int(ts) for ts, _ in datas])

            given_value = 0.0  # Replace with your desired value
            #given_value = 1716985520.148 # Replace with your desired value

            greater_than_value = timestamps[timestamps > given_value]
            less_than_value = timestamps[timestamps <= given_value]

            values = [float(value) for _, value in datas]

            last_ten_values = values[-(len(greater_than_value)):]

            greater_than_valueReduce = greater_than_value
            last_ten_valuesReduce = last_ten_values

            #lissageValues = smooth(last_ten_valuesReduce)
            lissageValues = last_ten_valuesReduce

            color = get_color_for_service(label)

            plt.plot(greater_than_valueReduce, lissageValues, color=color, label=label)
            return greater_than_valueReduce
        return []


    def plot_jsonMemory(file_name, label):
        with open(file_name, 'r') as file:
            json_data = json.load(file)

        if len(json_data['data']['result']) > 0:
            datas = json_data['data']['result'][0]['values']

            timestamps = np.array([int(ts) for ts, _ in datas])

            given_value = 0.0  # Replace with your desired value
            # given_value = 1716985520.148 # Replace with your desired value

            greater_than_value = timestamps[timestamps > given_value]
            less_than_value = timestamps[timestamps <= given_value]

            values = [float(value) for _, value in datas]

            # Normaliser les valeurs en gibibytes (GiB)
            normalized_values = []
            for value in values:
                value_in_bytes = value   # Convertir en octets
                value_in_gib = value_in_bytes / (1000 ** 3)  # Convertir en GiB
                normalized_values.append(value_in_gib)  # Arrondir à 2 décimales
                #normalized_values.append(round(value_in_gib, 2))  # Arrondir à 2 décimales

            last_ten_values = normalized_values[-(len(greater_than_value)):]

            greater_than_valueReduce = greater_than_value
            last_ten_valuesReduce = last_ten_values

            # lissageValues = smooth(last_ten_valuesReduce)
            lissageValues = last_ten_valuesReduce

            color = get_color_for_service(label)

            plt.plot(greater_than_valueReduce, lissageValues, color=color, label=label)
            return greater_than_valueReduce
        return []


    # Initialize the plot
    plt.figure(figsize=(10, 16))

    # Plot the first set of data
    plt.subplot(4, 1, 1)
    all_timestamps = []

    today = date.today()
    dir_name = today.strftime("%d-%m-%Y")

    #save_graphics_at = f"../Plots/{dir_name}"  #TFB8500
    #save_graphics_at = f"../Plots"  #TFB8500
    # he directory where you want things to be saved
    if not os.path.exists(save_graphics_at):
        os.makedirs(save_graphics_at)

    directory = save_path + 'cpu'
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        #for file_name in json_files1:
        file_parts = file_path.split("/")
        last_part = (file_parts[-1]).split(".")[0]
        result = re.split(r'-\d+', last_part)[0]
        timestamps = plot_json(file_path, last_part)

        if len(timestamps) > 0:
            all_timestamps.append(timestamps)

    # Concatenate all timestamps
    all_timestamps = np.concatenate(all_timestamps)

    # Calculate the start and end times
    start_time = min(all_timestamps)
    end_time = max(all_timestamps)

    # Generate a list of ticks every 20 seconds
    ticks = np.arange(start_time, end_time + 1, plot_window)

    # Set ticks on the x-axis
    ticks_seconds = [((ts - start_time) // plot_window) * plot_window for ts in ticks]

    print("max cpu")
    print(len(ticks_seconds))
    plt.axhline(y=1, color='r', linestyle='--')
    plt.xticks(ticks, ticks_seconds)
    plt.xlabel('Time (seconds)')
    plt.ylabel('cores per second')
    plt.title('CPU usage')
    plt.ylim(0, cpu_limit_max)
    #plt.grid(True)
    plt.xticks(rotation=45)
    #plt.legend()

    # Plot the second set of data
    plt.subplot(4, 1, 2)
    all_timestamps2 = []

    directory2 = save_path + 'memory'
    for file_name in os.listdir(directory2):
        file_path = os.path.join(directory2, file_name)
        #for file_name in json_files1:
        file_parts = file_path.split("/")
        last_part = (file_parts[-1]).split(".")[0]
        result = re.split(r'-\d+', last_part)[0]
        timestamps2 = plot_jsonMemory(file_path, last_part)

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
    #plt.legend()

    lastEl = ticks_seconds2[-1]

    plt.subplot(4, 1, 3)

    resultat = ticks_seconds2[3:]

    test = 0

    try:
        df = pd.read_csv(plot_path + fileToPlot)
    except FileNotFoundError:
        #print(f"Le fichier {file_name} n'a pas été trouvé dans le chemin {plot_path}")
        # Vous pouvez également faire d'autres traitements ici, comme retourner un DataFrame vide
        df = pd.DataFrame()

    #df = pd.DataFrame()

    nombre_lignes = len(df)

    print("nombre de ligne "+str(nombre_lignes))

    lastEl = 600
    # if nombre_lignes > 0:
    #     test = nombre_lignes
    #if nombre_lignes > lastEl:
    test = nombre_lignes

    nouvelles_lignes = []

    #lastEl = 1202

    if test < lastEl:
        print("ligne dedans "+str(test))
        for i in range(test + 1, lastEl + 1):
            #for i in range(0, lastEl+1):
            target_time = i + 0.5
            nouvelle_ligne = pd.DataFrame([[target_time, 0, 0, 0, 0, 0, 0]],
                                          columns=['Target Time', 'Load Intensity', 'Successful Transactions',
                                                   'Failed Transactions', 'Dropped Transactions', 'Avg Response Time',
                                                   'Final Batch Dispatch Time'])
            nouvelles_lignes.append(nouvelle_ligne)

        df = pd.concat([df] + nouvelles_lignes, ignore_index=True)
    elif lastEl > 0:
        df = df.head(int(lastEl))
        target_time = lastEl + 0.5
        nouvelle_ligne = pd.DataFrame([[target_time, 0, 0, 0, 0, 0, 0]],
                                      columns=['Target Time', 'Load Intensity', 'Successful Transactions',
                                               'Failed Transactions', 'Dropped Transactions', 'Avg Response Time',
                                               'Final Batch Dispatch Time'])

        df = pd.concat([df] + [nouvelle_ligne], ignore_index=True)
        #df.to_csv(f"output{x}.csv", index=False)

    print("la taille actuelle "+str(len(df)))
    df['Target Time'] = df['Target Time'].astype(int)

    # Votre code pour créer le graphique
    line1, = plt.plot(df['Target Time'], df['Load Intensity'])
    line2, = plt.plot(df['Target Time'], df['Successful Transactions'], color='green')
    line3, = plt.plot(df['Target Time'], df['Failed Transactions'], color='red')
    # line4, = plt.plot(df['Target Time'], df['Dropped Transactions'])

    # Définition des emplacements des marqueurs d'axe personnalisés
    interval = plot_window
    plt.xticks(np.arange(min(df['Target Time']), max(df['Target Time']) + 1, interval))
    plt.xticks(rotation=45)
    #plt.legend([line1, line2, line3, line4], ['Load Intensity', 'Successful Transactions', 'Failed Transactions', 'Dropped Transactions'])
    plt.legend([line1, line2, line3, ], ['Load Intensity', 'Successful Transactions', 'Failed Transactions'])

    #plt.xlim(0, 6)  # Limites de l'axe des abscisses
    plt.ylim(0, load_max)  # Limites de l'axe des ordonnées

    plt.xlabel('Time (seconds)')
    plt.ylabel('Number of requests')
    plt.axhline(y=200, color='r', linestyle='--')
    plt.subplot(4, 1, 4)
    all_timestamps3 = []
    # Read JSON data from a file
    directory3 = save_path + 'pod_info/pod_info.json'

    with open(directory3, 'r') as file:
        source = json.load(file)

    timestamps = []
    values = []
    tab = []
    all_timestamps = []

    data_list = source['data']['result']

    legend_dict = {}

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

        legend_dict[deployment_name] = \
            line = plt.plot([], [], color=get_color_for_serviceInit(deployment_name), label=deployment_name)[0]
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
    plt.legend()

    plt.tight_layout()

    files = os.listdir(save_graphics_at)
    data_count = sum(1 for f in files if f.startswith("output") and f.endswith(".png"))
    my_string = f"{save_graphics_at}/output{str(data_count + 1)}-{fileToPlot}.png"

    #plt.legend(legend_dict.values(), legend_dict.keys(), loc='upper center', ncol=3)
    plt.legend(legend_objects, legend_labels, loc='upper center', ncol=3)

    plt.savefig(my_string)
    plt.show()
    x = x + 1
