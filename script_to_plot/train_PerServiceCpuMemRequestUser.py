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
    read_parameters_from_json, sort_legend, cpu_limit_max, memory_limit, colors_table, range_limit, plot_json_generic, \
    harmonization, plot_metrics, request_volume_limit, load_max

#metric_to_plot="request_aggr" #latency or request


#range_limit = 7

file_path_json = '../teastore.json'

csv_file_path = "/home/erods-chouette/Documents/synchronizeExperimentation/Load/load1/"

root_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/grenoble/train/22-11-2024/load1temp_profile_login_no_user_creation_at_beginning/hyperthreading/HomePage"

latency_path = root_path
print("root_path")
print(root_path)

services = ["ts-auth-service"]
#services = ["ts-inside-payment-service","ts-order-other-service","ts-auth-service","ts-ui-dashboard", "ts-order-other-service", "ts-station-service", "ts-travel-service", "ts-food-service", "ts-ticketinfo-service","ts-basic-service"]

#services = ["teastore-auth", "teastore-image", "teastore-persistence", "teastore-recommender", "teastore-registry","teastore-webui"]

elts = ["li_const_2"]
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
        #save_path = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/load2/nantes/hyperthreading/128/linear/3nodes/linear/mean_calculation/{x}/"
        #save_path = f"../nantes/hyperthreading/16-08-2024/data/metrics/experimentation-output-linear_80requests_max_per_sec.csv/"

        #save_graphics_at = f"/home/erods-chouette/Documents/synchronizeExperimentation/locust/load2/nantes/hyperthreading/128/linear/3nodes/linear/mean_calculation/{x}/Plots"
        save_graphics_at = f"{root_path}/{x}/Plots/merge"
        full_path = os.path.join(save_graphics_at, x)

        parameters = read_parameters_from_json(file_path_json)

        #cpu_step = parameters['CPU_STEP']

        plot_window = 50  # Show by interval of 5 minutes

        # Plot the first set of data
        plt.subplot(5, 1, 1)
        all_timestamps = []
        all_values = []

        today = date.today()
        dir_name = today.strftime("%d-%m-%Y")

        #save_graphics_at = f"../Plots/{dir_name}"  #TFB8500
        #save_graphics_at = f"../Plots"  #TFB8500
        # he directory where you want things to be saved
        if not os.path.exists(full_path):
            os.makedirs(full_path)

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
            timestamps, current_line, label = plot_json_generic(directory, element, data_type='cpu')


            if len(timestamps) > 0:
                all_timestamps.append(timestamps)
                #all_values.append(values)
            legend_objectsCpu.append(current_line)
            legend_labelsCpu.append(label)
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
        plt.subplot(5, 1, 2)
        all_timestamps2 = []

        legend_objectsMemory = []
        legend_labelsMemory = []

        directoryS2 = save_path + 'memory/'

        #listElement = ['teastore-persistence']

        for element in listElement:
            directory2 = save_path + f"memory/{element}/"
            file_path = os.path.join(directory2, element)
            file_parts = file_path.split("/")
            last_part = (file_parts[-1]).split(".")[0]
            result = re.split(r'-\d+', last_part)[0]
            timestamps2, current_line, label = plot_json_generic(directory2, last_part, data_type='memory')

            if len(timestamps2) > 0:
                all_timestamps2.append(timestamps2)

            legend_objectsMemory.append(current_line)
            legend_labelsMemory.append(label)


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
        #plt.ylim(0, memory_limit)
        #plt.grid(True)
        plt.xticks(rotation=45)

        # Séparer les objets et les labels après le tri
        legend_objects_sorted, legend_labels_sorted = sort_legend(legend_objectsMemory, legend_labelsMemory)

        #plt.legend(legend_objects_sorted, legend_labels_sorted)
        plt.legend()
        lastEl = ticks_seconds2[-1]

        plt.subplot(5, 1, 3)

        max_value=0

        json_filenames = []
        plot_stats_path=""
        # retrieve the max size to pyt ylim for all plots
        for idx, svc in enumerate(services):
            json_file_path = os.path.join(latency_path,"request_aggr", svc, x)
            json_filenames = sorted([os.path.join(json_file_path, file) for file in
                              os.listdir(json_file_path)[:range_limit]])  # Take the first 3 elements

            for json_filename in json_filenames:
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

        for idx, svc in enumerate(listElement):


            json_file_path = os.path.join(latency_path, "request_aggr", svc, x)

            json_filenames = sorted([os.path.join(json_file_path, file) for file in
                              os.listdir(json_file_path)[:range_limit]])

            max_value = math.ceil(max_value / 100) * 100

            for json_filename in json_filenames:
                position = json_filenames.index(json_filename)
                file_name_with_extension = os.path.basename(json_filename)
                file_name, _ = os.path.splitext(file_name_with_extension)

                # Charger le JSON depuis un fichier
                with open(json_filename) as f:
                    data = json.load(f)

                timestamps = []

                plot_metrics(data, svc, int(position), "request_aggr")

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


            #plt.plot(time, values, color='green', label='Load Intensity')
            #plt.axhline(y=200, color='r', linestyle='--')
            plt.xlabel('Time (seconds)')
            plt.ylabel('rps')
            plt.title('Request volume')
            plt.ylim(0, request_volume_limit)

            for i in range(1,range_limit+1):
                plot_stats_path = f"{root_path}/output/{x}_{i}_stats_history.csv"
                print("le chemin")
                print(plot_stats_path)

                df_stats = pd.read_csv(plot_stats_path)

                requests = df_stats['Requests/s']
                requests = requests.reindex(range(299), fill_value=0)
                print(requests)
                print("le tem")
                print(time)

                plt.plot(time, requests,  color=colors_table[i-1], linestyle=line_styles[(i-1) % len(line_styles)], label=f"locust_stats_{i}")
                #plt.plot(time, requests)

            plt.legend(loc='upper left', ncol=4, frameon=False)

#-------------------------------------------------------------------------
        plt.subplot(5, 1, 4)

        max_value = 0

        json_filenames = []

        # retrieve the max size to pyt ylim for all plots
        for idx, svc in enumerate(services):
            json_file_path = os.path.join(latency_path, "request_aggr", svc, x)
            json_filenames = sorted([os.path.join(json_file_path, file) for file in
                                     os.listdir(json_file_path)[:4]])  # Take the first 3 elements

            for json_filename in json_filenames:
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

        plt.plot(time, values, color='green', label='Expected users')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Number of users')
        plt.title('Creation of users for load injection')
        plt.ylim(0, load_max)


        df_stats = pd.read_csv(plot_stats_path)

        # print(df_stats.iloc[0])
        print("nombre de ligne " + str(len(df_stats['User Count'])))
        # print(df_stats['Timestamp'])
        # df_stats = pd.DataFrame()


        for i in range(1, range_limit+1):
            plot_stats_path = f"{root_path}/output/{x}_{i}_stats_history.csv"

            df_stats = pd.read_csv(plot_stats_path)

            user_count = df_stats['User Count']
            user_count = user_count.reindex(range(299), fill_value=0)

            plt.plot(time, user_count, color=colors_table[i - 1], linestyle=line_styles[(i-1) % len(line_styles)],  label=f"active_users_{i}")
        plt.legend(loc='upper left', frameon=False)

#-------------------------------------------------------------------------
        plt.subplot(5, 1, 5)

        max_value = 0

        json_filenames = []

        # retrieve the max size to pyt ylim for all plots
        for idx, svc in enumerate(services):
            json_file_path = os.path.join(latency_path, "latency", svc, x)
            json_filenames = sorted([os.path.join(json_file_path, file) for file in
                                     os.listdir(json_file_path)[:range_limit]])  # Take the first 3 elements

            for json_filename in json_filenames:
                #print(json_filename)
                with open(json_filename) as f:
                    source = json.load(f)
                data_list = source['data']['result']
                for json_data in data_list:
                    result = json_data
                    # values = [float(x[1]) for x in result["values"]]
                    values = [float(x[1]) for x in result["values"] if x[1] != "NaN"]
                    if values:  # Check if values is not empty
                        #print(max(values))
                        if max(values) > max_value:
                            max_value = max(values)


        for idx, svc in enumerate(listElement):
            json_file_path = os.path.join(latency_path, "latency", svc, x)

            json_filenames = sorted([os.path.join(json_file_path, file) for file in
                                     os.listdir(json_file_path)[:range_limit]])
            max_value = math.ceil(max_value / 100) * 100

            for json_filename in json_filenames:
               # print("***************************************************")
                #print(json_filenames)
                #print(len(json_filename))
                position = json_filenames.index(json_filename)
                file_name_with_extension = os.path.basename(json_filename)
                file_name, _ = os.path.splitext(file_name_with_extension)


                # Charger le JSON depuis un fichier
                with open(json_filename) as f:
                    data = json.load(f)

                timestamps = []

                plot_metrics(data, svc, int(position), "latency")
            plt.legend(ncol=2)
            plt.title('Request duration')
            plt.xlabel('Time (seconds)')
            plt.ylabel('Latency (ms)')
            #plt.yscale('log')
            plt.ylim(0, max_value)

        plt.tight_layout()

        files = os.listdir(save_graphics_at)

        data_count = sum(1 for f in files if f.startswith("output") and f.endswith(".png"))
        #my_string = f"{save_graphics_at}/output{str(data_count + 1)}-{x}.png"
        my_string = f"{save_graphics_at}/{x}/output{str(data_count + 1)}-{element}.png"
        print(my_string)
        #plt.savefig(my_string)
        plt.show()
        plt.close(fig)
