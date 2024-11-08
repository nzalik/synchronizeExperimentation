import json
import math
import matplotlib.pyplot as plt
from datetime import datetime
import os
import numpy as np
from utils.constants import get_color_for_serviceInit, normalization, line_styles, plot_limit, smooth, open_file, \
    read_parameters_from_json, sort_legend, cpu_limit_max, memory_limit


metric_to_plot="request" #latency or request
harmonization=False

latency_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/warm_equal_load/nantes/hyperthreading/128/linear/3nodes/linear/31-10-2024/{metric_to_plot}/"

file_name=""


def plot_metrics(data, ax):
    global timestamps
    results = data['data']['result']

    for result in results:
        metric = result['metric']
        source_workload = metric.get('source_workload', 'unknown')
        destination = metric.get('destination_workload', elt)

        source_workload_txt = source_workload.split('-')[1] if '-' in source_workload else source_workload
        destination_txt = destination.split('-')[1]

        timestamps = np.arange(0, plot_limit)
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

        color = get_color_for_serviceInit(source_workload)
        ax.plot(timestamps, values, color=color,
                label=f'{source_workload_txt + str(position + 1)} → {destination_txt + str(position + 1)}{multiplier_note}',
                linestyle=line_styles[position])

    start_time = min(timestamps)
    end_time = max(timestamps)

    ticks = np.arange(start_time, end_time + 1, plot_window)
    ticks_seconds = [((ts - start_time) // plot_window) * plot_window for ts in ticks]
    ax.set_xticks(ticks)
    ax.set_xticklabels(ticks_seconds)

    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('rps (requests per second)')
    ax.set_title(f'Request volume')
    #ax.set_title(f'Requests volume send to {elt}')
    if metric_to_plot=="latency":
        ax.set_ylabel('Latency (ms)')
        ax.set_title(f'Request duration')
        #ax.set_title(f'Request duration to {elt}')

    ax.set_ylim(0, max_value)
    ax.legend(loc='upper left', frameon=False)
    return ticks

#axes = axes.flatten()
json_files = ["si_sin_2", "linear_100", "li_stairsd_2", "li_stairsu_2"]
#json_files = ["linear_100","li_stairsd_2","li_stairsu_2","rd_jump_2","rd_stairs_2","si_abscos_2","si_abssin_2","si_cos_2","si_sin_2"]
max_value=0

for json_file in json_files:
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    save_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/warm_equal_load/nantes/hyperthreading/128/linear/3nodes/linear/31-10-2024/{json_file}/Plots/{metric_to_plot}"

    # retrieve the max size to pyt ylim for all plots
    for idx, elt in enumerate(
            ["teastore-auth", "teastore-recommender", "teastore-image", "teastore-persistence", "teastore-registry", "teastore-webui"]):
        json_file_path = os.path.join(latency_path, elt, json_file)
        json_filenames = [os.path.join(json_file_path, file) for file in
                          os.listdir(json_file_path)[:3]]  # Take the first 3 elements

        for json_filename in json_filenames:
            print(json_filename)
            with open(json_filename) as f:
                source = json.load(f)
            data_list = source['data']['result']
            for json_data in data_list:
                result = json_data
                #values = [float(x[1]) for x in result["values"]]
                values = [float(x[1]) for x in result["values"] if x[1] != "NaN"]
                if values:  # Check if values is not empty
                    print(max(values))
                    if max(values) > max_value:
                        max_value = max(values)

    #max_value = 10000
    print("on est la pour")
    print(json_file)
    print(max_value)
    print(
        "------------------------------------------------------------------------------------------------------------------------")
    for idx, elt in enumerate(
            ["teastore-auth", "teastore-recommender", "teastore-image", "teastore-persistence", "teastore-registry", "teastore-webui"]):
        json_file_path = os.path.join(latency_path, elt, json_file)

        json_filenames = [os.path.join(json_file_path, file) for file in
                          os.listdir(json_file_path)[:3]]  # Take the first 3 elements
        #print(json_filenames)
        max_value = math.ceil(max_value / 100) * 100

        for json_filename in json_filenames:
            position = json_filenames.index(json_filename)
            file_name_with_extension = os.path.basename(json_filename)
            file_name, _ = os.path.splitext(file_name_with_extension)

            # Charger le JSON depuis un fichier
            with open(json_filename) as f:
                data = json.load(f)

            plot_window = 150
            timestamps = []

            plot_metrics(data, axes[idx])
    plt.tight_layout()
    os.makedirs(save_path, exist_ok=True)
    chemin=""
    if harmonization and metric_to_plot == "latency":
        chemin = save_path + "/" + file_name + "_harmonization.png"
    else:
        chemin = save_path + "/" + file_name + "_combined.png"
    plt.savefig(chemin)
    plt.show()
    plt.close(fig)  # Closing the figure to avoid overlap with the next iteration

    print("*********************************iteration*********************************************************")
