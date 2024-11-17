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

from utils.constants import get_color_for_service_init, normalization, line_styles, plot_limit, smooth, open_file, \
    read_parameters_from_json, sort_legend, cpu_limit_max, memory_limit, colors_table

#metric_to_plot="request_aggr" #latency or request
harmonization=False
range_limit = 2

file_path_json = '../teastore.json'

csv_file_path = "/home/erods-chouette/Documents/synchronizeExperimentation/Load/load2/"


root_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/nantes/socialNetwork/16-11-2024/social_load_sequential_restart/hyperthreading"
latency_path = f"{root_path}"

services = ["compose-post-service"]
#services = ["teastore-auth", "teastore-image", "teastore-persistence", "teastore-recommender", "teastore-registry","teastore-webui"]

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
    json_data_file4 = open_file(os.path.join(file_path, list_element[3]))
    json_data_file5 = open_file(os.path.join(file_path, list_element[4]))
    json_data_file6 = open_file(os.path.join(file_path, list_element[5]))
    json_data_file7 = open_file(os.path.join(file_path, list_element[6]))
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
        datas4 = json_data_file4['data']['result'][0]['values']
        datas5 = json_data_file5['data']['result'][0]['values']
        datas6 = json_data_file6['data']['result'][0]['values']
        datas7 = json_data_file7['data']['result'][0]['values']
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
        values4 = [float(value) for _, value in datas4]
        values5 = [float(value) for _, value in datas5]
        values6 = [float(value) for _, value in datas6]
        values7 = [float(value) for _, value in datas7]
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
        values4 = np.array(smooth(values4))
        values5 = np.array(smooth(values5))
        values6 = np.array(smooth(values6))
        values7 = np.array(smooth(values7))
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
        if is_cpu:
            legend_objectsCpu.append(current_line)
            legend_labelsCpu.append(label)
        else:
            legend_objectsMemory.append(current_line)
            legend_labelsMemory.append(label)

        #temp_list = [values1, values2]
        temp_list = [values1, values2,  values4, values5, values6, values7][:range_limit]
        for index, tab in enumerate(temp_list):
            print(index)
            #tab = temp_list[i-1]
            if is_cpu:
                plt.plot(new_timestamps, tab, color = colors_table[index], label=label+str(index+1), linestyle=line_styles[index % len(line_styles)])
            else:
                plt.plot(new_timestamps, normalization(tab), color = colors_table[index], label=label+str(index+1), linestyle=line_styles[index % len(line_styles)])

        #plt.plot(new_timestamps, lissageValues, color=color, label=label)
        return new_timestamps
        #return new_timestamps, lissageValues if is_cpu else new_timestamps
    return []


elts = ["li_linear_2"]
#elts = ["li_stairsu_2","li_stairsd_2","li_stairsu_2","si_sin_2"]
#elts = ["li_const_2","linear_10", "li_stairsd_2","li_stairsu_2","si_sin_2"]
#elts = ["li_const_2","linear_50","li_stairsd_2","li_stairsu_2","rd_bell_2","rd_jump_2","rd_stairs_2","si_abscos_2","si_abssin_2","si_cos_2","si_log_2","si_sin_2"]
#elts = [180, 200, 250, 300, 350]
#x = 1


#element="teastore-webui"
#listElement = services

for element in services:
    # Initialize the plot
    fig = plt.figure(figsize=(10, 16))
    #element = "teastore-webui"
    listElement = [element]
    for x in elts:

        print(x)
        fileToPlot = f"output_{x}"
        #fileToPlot = f"output-linear_{x}requests_max_per_sec.csv"
        #fileToPlot = f"output-linear_80requests_max_per_sec.csv"
        save_path = f"{root_path}/{x}/"
        #save_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/load1/nantes/hyperthreading/128/linear/3nodes/linear/mean_calculation/{x}/"
        #save_path = f"../nantes/hyperthreading/16-08-2024/data/metrics/experimentation-output-linear_80requests_max_per_sec.csv/"

        #save_graphics_at = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/load1/nantes/hyperthreading/128/linear/3nodes/linear/mean_calculation/{x}/Plots"
        save_graphics_at = f"{root_path}/{x}/Plots/merge"

        parameters = read_parameters_from_json(file_path_json)

        #cpu_step = parameters['CPU_STEP']

        plot_window = 50  # Show by interval of 5 minutes

        # Plot the first set of data
        plt.subplot(1, 1, 1)
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


        #listElement = os.listdir(directoryS)
       # print("all les elements")
        #print(listElement)

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

        #plt.axhline(y=1, color='r', linestyle='--')
        plt.xticks(ticks, ticks_seconds)
        plt.xlabel('Time (seconds)')
        plt.ylabel('cores per second')
        plt.title('CPU usage')
        #plt.ylim(0, cpu_limit_max)
        #plt.grid(True)
        plt.xticks(rotation=45)

        # Séparer les objets et les labels après le tri
        legend_objects_sorted2, legend_labels_sorted2 = sort_legend(legend_objectsCpu, legend_labelsCpu)

        #plt.legend(legend_objects_sorted2, legend_labels_sorted2)

        plt.legend()

        # Plot the second set of data


        plt.tight_layout()

        files = os.listdir(save_graphics_at)
        data_count = sum(1 for f in files if f.startswith("output") and f.endswith(".png"))
        #my_string = f"{save_graphics_at}/output{str(data_count + 1)}-{x}.png"
        my_string = f"{save_graphics_at}/output{str(data_count + 1)}-{element}.png"
        print(my_string)
        plt.savefig(my_string)
        plt.show()
        plt.close(fig)
