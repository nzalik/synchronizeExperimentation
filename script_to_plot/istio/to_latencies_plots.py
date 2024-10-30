import json
import matplotlib.pyplot as plt
from datetime import datetime
import os
import numpy as np
# Exemple de données JSON (remplace par tes données réelles)

plot_window = 60
timestamps = []


# Fonction pour traiter et tracer les données
def plot_metrics(data):
    # Extraire les résultats
    global timestamps
    results = data['data']['result']

    # Pour chaque métrique dans les résultats
    for result in results:
        metric = result['metric']
        source_workload = metric.get('source_workload', 'unknown')

        # Extraire les timestamps et les valeurs
        timestamps = [point[0] for point in result['values']]  # Timestamps
        values = [0 if point[1] == "NaN" else float(point[1]) for point in result['values']]  # Remplacer NaN par 0

        # Convertir les timestamps en format heure lisible
        heures = [datetime.fromtimestamp(ts).strftime('%M') for ts in timestamps]

        color = get_color_for_serviceInit(source_workload)
        # Plotter les données
        plt.plot(timestamps, values, color=color, label=f'{source_workload}')

    # Ajouter des labels et une légende
    workload_name = "teastore-webui"
    start_time = min(timestamps)
    end_time = max(timestamps)

    ticks = np.arange(start_time, end_time + 1, plot_window)
    ticks_seconds = [((ts - start_time) // plot_window) * plot_window for ts in ticks]
    plt.xticks(ticks, ticks_seconds)

    plt.xlabel('Time (minutes)')
    plt.ylabel('Latency (ms)')
    plt.title('Latency from others services to ' + name)
    plt.legend()
    racine = os.path.dirname("json_filename") + "/Plots"

    file_racine, _ = os.path.splitext(os.path.basename("json_filename"))
    resultat = f"/{file_racine}.png"

    os.makedirs(racine, exist_ok=True)
    output_filename = racine + resultat

    print("on save")
    print(output_filename)
    print(resultat)
    print(racine)
    # Afficher le graphique
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.show()


# with open(json_filename) as f:
#     data = json.load(f)

def open_file(file_name):
    with open(file_name, 'r') as file:
        #for file_name in files:
        #with open(file_name, 'r') as file:
        json_data = json.load(file)
        return json_data

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

plot_limit=301
latency_path = "/home/erods-chouette/Documents/synchronizeExperimentation/locust/organised/nantes/hyperthreading/128/linear/3nodes/linear/26-10-2024/latency"
name='teastore-auth'
json_files = ["linear_100", "li_stairsd_2", "li_stairsu_2", "rd_jump_2", "rd_stairs_2","si_abscos_2", "si_abssin_2"]
#"si_cos_2" "si_sin_2" not enough value
for json_file in json_files:
    print("**********************************************************************************")
    for directory in ["teastore-auth", "teastore-recommender", "teastore-image", "teastore-persistence",
                      "teastore-registry"]:
        json_file_path = os.path.join(latency_path, directory, json_file)
        print("le chemin")
        print(json_file_path)

        list_element = os.listdir(json_file_path)
        print(list_element)

        json_data_files = [open_file(os.path.join(json_file_path, file)) for file in list_element]

        for i, json_data_file in enumerate(json_data_files, 1):
            print(f"json_data_file{i}", json_data_file)

        if all('data' in json_data_file and 'result' in json_data_file['data'] and len(
                json_data_file['data']['result']) > 0
               for json_data_file in json_data_files):
            datas_list = []
            source_workload_list = []
            for json_data_file in json_data_files:
                for result in json_data_file['data']['result']:
                    if result['values'] not in datas_list:  # Ensure uniqueness in datas_list
                        datas_list.append(result['values'])
                    metric = result['metric']
                    source_workload = metric.get('source_workload', 'unknown')
                    if source_workload not in source_workload_list:  # Ensure uniqueness in source_workload_list
                        source_workload_list.append(source_workload)

            print("la liste de workload")
            print(source_workload_list)
            selected_values = []

            timestamps = np.array([int(ts) for ts, _ in selected_values])
            given_value = 0.0

            greater_than_value = timestamps[timestamps > given_value]

            values_list = [values[:plot_limit] for values in
                           [[0 if value == "NaN" else float(value) for _, value in datas] for datas in datas_list] if
                           len(values) >= plot_limit][:2]

            print("###########les valeurs#######################")
            for values in values_list:
                print(values)
                print(len(values))

            values_arrays = [np.array(values) for values in values_list]
            meanValues = np.mean(values_arrays, axis=0)

            new_timestamps = np.arange(0, plot_limit)

            color = get_color_for_serviceInit("teastore-auth")

            current_line = plt.plot([], [], color=color, label="")[0]
            plt.plot(new_timestamps, meanValues, color=color, label=source_workload_list[0])

        # Appeler la fonction pour tracer les données pour chaque fichier JSON
        # with open(json_file_path) as f:
        #     data = json.load(f)
        # plot_metrics(data)
#plot_metrics(data)

plt.title('Comparison of latency between different services')
plt.xlabel('Time (s)')
plt.ylabel('Latency (ms)')
plt.title('Latency from others services to ' + name)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output_filename_2222222222222.png")
plt.show()