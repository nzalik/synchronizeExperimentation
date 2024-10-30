import json
import matplotlib.pyplot as plt
from datetime import datetime
import os
import numpy as np


# Exemple de données JSON (remplace par tes données réelles)
name = 'teastore-auth'
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

latency_path = "/home/erods-chouette/Documents/synchronizeExperimentation/locust/organised/nantes/hyperthreading/128/linear/3nodes/linear/26-10-2024/latency"
file_name=""

plot_limit = 301
line_styles=["solid","dotted","dashed","dashdot"]
axes = axes.flatten()
json_files = ["si_sin_2"]
#json_files = ["linear_100", "li_stairsd_2", "li_stairsu_2", "rd_jump_2", "rd_stairs_2","si_abscos_2", "si_abssin_2"]

#Plotting by profiles
for json_file in json_files:
    save_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/organised/nantes/hyperthreading/128/linear/3nodes/linear/26-10-2024/{json_files[0]}/Plots/latencies"

    for idx, elt in enumerate(["teastore-auth", "teastore-recommender", "teastore-image", "teastore-persistence"]):
        json_file_path = os.path.join(latency_path, elt, json_file)
        print(json_file_path)

        json_filenames = [os.path.join(json_file_path, file) for file in
                          os.listdir(json_file_path)[:3]]  # Take the first 3 elements
        i=0
        for json_filename in json_filenames:

            print(json_filename)
            file_name_with_extension = os.path.basename(json_filename)
            file_name, _ = os.path.splitext(file_name_with_extension)

            # Charger le JSON depuis un fichier
            with open(json_filename) as f:
                data = json.load(f)


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
                        return '#265DAB'
                    case 'teastore-recommender':
                        return '#CB2027'
                    case _:
                        return 'black'


            plot_window = 60
            timestamps = []


            # Fonction pour traiter et tracer les données
            def plot_metrics(data, ax):
                global timestamps
                results = data['data']['result']

                for result in results:
                    metric = result['metric']
                    source_workload = metric.get('source_workload', 'unknown')

                    #timestamps = [point[0] for point in result['values']]  # Timestamps
                    timestamps = np.arange(0, plot_limit)
                    values = [0 if point[1] == "NaN" else float(point[1]) for point in
                              result['values'][:plot_limit]] + [0] * (
                                     plot_limit - min(plot_limit, len(result['values'])))  # Remplacer NaN par 0 et compléter avec des 0 si nécessaire

                    heures = [datetime.fromtimestamp(ts).strftime('%M') for ts in timestamps]

                    color = get_color_for_serviceInit(source_workload)
                   # plt.axhline(y=1, color='r', linestyle='--')
                    ax.plot(timestamps, values, color=color, label=f'{source_workload}', linestyle=line_styles[i])

                start_time = min(timestamps)
                end_time = max(timestamps)

                ticks = np.arange(start_time, end_time + 1, plot_window)
                ticks_seconds = [((ts - start_time) // plot_window) * plot_window for ts in ticks]
                ax.set_xticks(ticks)
                ax.set_xticklabels(ticks_seconds)

                ax.set_xlabel('Time (seconds)')
                ax.set_ylabel('Latency (ms)')
                ax.set_title(f'Latency from others services to {elt}')
                ax.legend()


            i = i + 1
            plot_metrics(data, axes[idx])

plt.tight_layout()
print(file_name)
os.makedirs(save_path, exist_ok=True)
chemin = save_path + "/" + file_name + "_combined.png"
print("le chemin")
print(chemin)
plt.savefig(chemin)
plt.show()
