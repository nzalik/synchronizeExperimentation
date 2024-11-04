#This is almostthe sme script as unified plot
#But I want to merge all graphics on the same plot

import json
import math
import os
import re
from datetime import date
from operator import index, indexOf
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils.constants import get_color_for_serviceInit, normalization, line_styles, plot_limit, smooth, open_file, \
    read_parameters_from_json, sort_legend, cpu_limit_max, memory_limit

#metric_to_plot="request" #latency or request
harmonization=False

file_path_json = '../teastore.json'

csv_file_path = "/home/erods-chouette/Documents/synchronizeExperimentation/Load/teastore_loads/"

latency_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/weekend/nantes/hyperthreading/128/linear/3nodes/linear/02-11-2024/"


def plot_json_generic(file_path, file_name, data_type='cpu'):
    is_cpu = data_type == 'cpu'
    label = file_name
    list_element = sorted(os.listdir(file_path))

    print("***************************************************alignement")
    print(list_element)

    print(list_element[0])
    json_data_file1 = open_file(os.path.join(file_path, list_element[0]))
    print(list_element[1])
    json_data_file2 = open_file(os.path.join(file_path, list_element[1]))
    print(list_element[2])
    json_data_file3 = open_file(os.path.join(file_path, list_element[2]))
    #json_data_file4 = open_file(os.path.join(file_path, list_element[3]))
    #json_data_file5 = open_file(os.path.join(file_path, list_element[4]))

    print(json_data_file1)
    print(json_data_file2)
    print(json_data_file3)
    #print(json_data_file4)

    if len(json_data_file1['data']['result']) > 0 and len(json_data_file2['data']['result']) > 0 and len(
            json_data_file3['data']['result']) > 0:
        datas1 = json_data_file1['data']['result'][0]['values']
        datas2 = json_data_file2['data']['result'][0]['values']
        datas3 = json_data_file3['data']['result'][0]['values']
       # datas4 = json_data_file4['data']['result'][0]['values']
        #datas5 = json_data_file5['data']['result'][0]['values']

        selected_values=[]

        valid_values_list = [datas1, datas2, datas3]
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
        #values4 = [float(value) for _, value in datas4]
        #values5 = [float(value) for _, value in datas5]

        print("###########les valeurs#######################")
        print(values1)
        print(values2)
        print(values3)
        #print(values4)

        print("******************completion*************************")
        longueur_max = plot_limit
        # longueur_max = max(len(liste) for liste in [values1, values2, values3])
        for liste in [values1, values2, values3]:
            if len(liste) > longueur_max:
                # Couper pour garder les longueur_max derniers éléments
                del liste[:-longueur_max]
            # else:
            #     # Compléter avec des zéros jusqu'à longueur_max
            #     while len(liste) < longueur_max:
            #         liste.append(0)


        values1 = np.array(smooth(values1))
        values2 = np.array(smooth(values2))
        values3 = np.array(smooth(values3))
        #values4 = np.array(values4)
        #values5 = np.array(values5)

        print(len(values1))
        print(len(values2))
        print(len(values3))
        #print(len(values4))
        #print(len(values5))

        meanValues = np.mean([values1, values2, values3], axis=0)

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

        temp_list = [values1, values2, values3]
        #temp_list = [values1, values2, values3]
        for index, tab in enumerate(temp_list):
            #tab = temp_list[i-1]
            if is_cpu:
                plt.plot(new_timestamps, tab, color=color, label=label+str(index+1), linestyle=line_styles[index])
            else:
                plt.plot(new_timestamps, normalization(tab), color=color, label=label+str(index+1), linestyle=line_styles[index])

        #plt.plot(new_timestamps, lissageValues, color=color, label=label)
        return new_timestamps
        #return new_timestamps, lissageValues if is_cpu else new_timestamps
    return []

def plot_metrics(data, elt, metric_to_plot=""):
    global timestamps
    results = data['data']['result']

    for result in results:
        metric = result['metric']
        source_workload = metric.get('source_workload', 'unknown')
        destination = metric.get('destination_workload', elt)

        source_workload_txt = source_workload.split('-')[1] if '-' in source_workload else source_workload
        destination_txt = destination.split('-')[1]

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


        print("la tialle ##############################""")
        print(len(valuesInit))
        print("###########################################")

        values = smooth(valuesInit)
        heures = [datetime.fromtimestamp(ts).strftime('%M') for ts in timestamps]

        color = get_color_for_serviceInit(source_workload)
        plt.plot(timestamps, values, color=color,
                label=f'{source_workload_txt + str(position + 1)} → {destination_txt + str(position + 1)}{multiplier_note}',
                linestyle=line_styles[position])




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


    return ticks


elts = ["linear_50"]
#elts = ["rd_stairs_2"]
#elts = ["linear_100","li_stairsd_2","li_stairsu_2","rd_jump_2","rd_stairs_2","si_abscos_2","si_abssin_2","si_cos_2","si_sin_2"]
#elts = [180, 200, 250, 300, 350]
#x = 1

for x in elts:

    print(x)
    fileToPlot = f"output_{x}"
    #fileToPlot = f"output-linear_{x}requests_max_per_sec.csv"
    #fileToPlot = f"output-linear_80requests_max_per_sec.csv"
    save_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/weekend/nantes/hyperthreading/128/linear/3nodes/linear/02-11-2024/{x}/"
    #save_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/advanced/nantes/hyperthreading/128/linear/3nodes/linear/mean_calculation/{x}/"
    #save_path = f"../nantes/hyperthreading/16-07-2024/data/metrics/experimentation-output-linear_80requests_max_per_sec.csv/"

    #save_graphics_at = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/advanced/nantes/hyperthreading/128/linear/3nodes/linear/mean_calculation/{x}/Plots"
    save_graphics_at = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/weekend/nantes/hyperthreading/128/linear/3nodes/linear/02-11-2024/{x}/Plots/merge"

    parameters = read_parameters_from_json(file_path_json)

    #cpu_step = parameters['CPU_STEP']

    plot_window = 50  # Show by interval of 5 minutes


    # Initialize the plot
    fig = plt.figure(figsize=(10, 16))

    # Plot the first set of data
    plt.subplot(5, 1, 1)
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

    listElement = ["teastore-webui"]
    #listElement = os.listdir(directoryS)
    print("all les elements")
    print(listElement)

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

    #plt.legend(legend_objects_sorted2, legend_labels_sorted2)

    plt.legend()

    # Plot the second set of data
    plt.subplot(5, 1, 2)
    all_timestamps2 = []

    legend_objectsMemory = []
    legend_labelsMemory = []

    directoryS2 = save_path + 'memory/'

    listElement = ['teastore-webui']

    for element in listElement:
        directory2 = save_path + f"memory/{element}/"
        file_path = os.path.join(directory2, element)
        print("lr chemon")
        print(file_path)
        #for file_name in json_files1:
        file_parts = file_path.split("/")
        last_part = (file_parts[-1]).split(".")[0]
        result = re.split(r'-\d+', last_part)[0]
        timestamps2 = plot_json_generic(directory2, last_part, data_type='memory')

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

    #plt.legend(legend_objects_sorted, legend_labels_sorted)
    plt.legend()
    lastEl = ticks_seconds2[-1]

    plt.subplot(5, 1, 3)

    # Define the variables `time` and `values` here before using them below
    time = []
    values = []
    try:
        df = pd.read_csv(csv_file_path + x + ".csv", sep=",")
        time = df.iloc[:, 0].tolist()
        values = df.iloc[:, 1].tolist()
    except FileNotFoundError:
        # print(f"Le fichier {file_name} n'a pas été trouvé dans le chemin {plot_path}")
        # Vous pouvez également faire d'autres traitements ici, comme retourner un DataFrame vide
        df = pd.DataFrame()

    # Data
    #time = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]
    #values = [132, 129, 132, 132, 132, 125, 128, 130, 129, 128]

    # Create the plot for 'Evolution of pods'
    plt.plot(time, values, color='#8ECAE6', label='Load Intensity')

    # Set labels and title
    plt.xlabel('Time (seconds)')
    plt.ylabel('rps')
    #plt.title('Evolution of pods')

    # Add legend
    plt.legend()

    plt.xticks(rotation=45)

    plt.subplot(5, 1, 4)

    #fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    #axes = axes.flatten()
    #save_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/warm_equal_load/nantes/hyperthreading/128/linear/3nodes/linear/31-10-2024/{json_file}/Plots/{metric_to_plot}"

    max_value=0

    json_filenames = []

    # retrieve the max size to pyt ylim for all plots
    for idx, svc in enumerate(
            ["teastore-auth", "teastore-recommender", "teastore-image", "teastore-persistence",
             "teastore-registry", "teastore-webui"]):
        json_file_path = os.path.join(latency_path,"request", svc, x)
        json_filenames = sorted([os.path.join(json_file_path, file) for file in
                          os.listdir(json_file_path)[:3]])  # Take the first 3 elements

        print(json_filenames)
        print(len(json_filenames[0]))
        print(len(json_filenames[1]))
        print(len(json_filenames[2]))

        for json_filename in json_filenames:
            print(json_filename)
            with open(json_filename) as f:
                source = json.load(f)
            data_list = source['data']['result']
            for json_data in data_list:
                result = json_data
                # values = [float(x[1]) for x in result["values"]]
                values = [float(x[1]) for x in result["values"] if x[1] != "NaN"]
                if values:  # Check if values is not empty
                    print(max(values))
                    if max(values) > max_value:
                        max_value = max(values)

    # max_value = 10000
    print("on est la pour")
    print(x)
    print(max_value)

    print(
        "------------------------------------------------------------------------------------------------------------------------")
    for idx, svc in enumerate(
            ["teastore-webui"]):
        json_file_path = os.path.join(latency_path, "request", svc, x)

        # json_filenames = sorted([os.path.join(json_file_path, file) for file in
        #                   os.listdir(json_file_path)[:1]])  # Take the first 3 elements
        # print(json_filenames)
        max_value = math.ceil(max_value / 100) * 100

        for json_filename in json_filenames:
            print("***************************************************")
            print(json_filenames)
            print(len(json_filename))
            position = json_filenames.index(json_filename)
            file_name_with_extension = os.path.basename(json_filename)
            file_name, _ = os.path.splitext(file_name_with_extension)

            # Charger le JSON depuis un fichier
            with open(json_filename) as f:
                data = json.load(f)

            timestamps = []

            plot_metrics(data, svc, "request")

        time = []
        values = []
        try:
            df = pd.read_csv(csv_file_path + x + ".csv", sep=",")
            time = df.iloc[:, 0].tolist()
            values = df.iloc[:, 1].tolist()
        except FileNotFoundError:
            # print(f"Le fichier {file_name} n'a pas été trouvé dans le chemin {plot_path}")
            # Vous pouvez également faire d'autres traitements ici, comme retourner un DataFrame vide
            df = pd.DataFrame()

        # Data
        # time = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]
        # values = [132, 129, 132, 132, 132, 125, 128, 130, 129, 128]

        # Create the plot for 'Evolution of pods'
        plt.plot(time, values, color='#8ECAE6', label='Load Intensity')
        plt.legend(loc='upper left', frameon=False)
    plt.subplot(5, 1, 5)

    # fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    # axes = axes.flatten()
    # save_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/warm_equal_load/nantes/hyperthreading/128/linear/3nodes/linear/31-10-2024/{json_file}/Plots/{metric_to_plot}"

    max_value = 0

    json_filenames = []

    # retrieve the max size to pyt ylim for all plots
    for idx, svc in enumerate(
            ["teastore-auth", "teastore-recommender", "teastore-image", "teastore-persistence",
             "teastore-registry", "teastore-webui"]):
        json_file_path = os.path.join(latency_path, "latency", svc, x)
        json_filenames = sorted([os.path.join(json_file_path, file) for file in
                                 os.listdir(json_file_path)[:3]])  # Take the first 3 elements

        print(json_filenames)
        print(len(json_filenames[0]))
        print(len(json_filenames[1]))
        print(len(json_filenames[2]))

        for json_filename in json_filenames:
            print(json_filename)
            with open(json_filename) as f:
                source = json.load(f)
            data_list = source['data']['result']
            for json_data in data_list:
                result = json_data
                # values = [float(x[1]) for x in result["values"]]
                values = [float(x[1]) for x in result["values"] if x[1] != "NaN"]
                if values:  # Check if values is not empty
                    print(max(values))
                    if max(values) > max_value:
                        max_value = max(values)

    # max_value = 10000
    print("on est la pour")
    print(x)
    print(max_value)

    print(
        "------------------------------------------------------------------------------------------------------------------------")
    for idx, svc in enumerate(
            ["teastore-webui"]):
        json_file_path = os.path.join(latency_path, "latency", svc, x)

        # json_filenames = sorted([os.path.join(json_file_path, file) for file in
        #                   os.listdir(json_file_path)[:1]])  # Take the first 3 elements
        # print(json_filenames)
        max_value = math.ceil(max_value / 100) * 100

        for json_filename in json_filenames:
            print("***************************************************")
            print(json_filenames)
            print(len(json_filename))
            position = json_filenames.index(json_filename)
            file_name_with_extension = os.path.basename(json_filename)
            file_name, _ = os.path.splitext(file_name_with_extension)

            # Charger le JSON depuis un fichier
            with open(json_filename) as f:
                data = json.load(f)

            timestamps = []

            plot_metrics(data, svc)

    plt.tight_layout()
    os.makedirs(save_path, exist_ok=True)
    chemin = ""
    if harmonization:
        chemin = save_path + "/" + file_name + "_harmonization.png"
    else:
        chemin = save_path + "/" + file_name + "_combined.png"
    plt.savefig(chemin)
    plt.show()
    #plt.close(fig)  # Closing the figure to avoid overlap with the next iteration

    print("*********************************iteration*********************************************************")

    #plt.legend(legend_objects, legend_labels, loc='upper center', ncol=2)

    plt.tight_layout()

    files = os.listdir(save_graphics_at)
    data_count = sum(1 for f in files if f.startswith("output") and f.endswith(".png"))
    my_string = f"{save_graphics_at}/output{str(data_count + 1)}-{x}.png"
    print(my_string)
    #plt.savefig(my_string)
    plt.show()
    plt.close(fig)
