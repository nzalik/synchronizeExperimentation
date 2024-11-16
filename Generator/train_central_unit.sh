#!/bin/bash

# Verify that the file is well loaded
if [ -z "$1" ]; then
    echo "Usage: $0 config_file.conf"
    exit 1
fi

# Charger le fichier de configuration
config_file="$1"
source "$config_file"

export PATH="$HOME/.local/bin:$PATH"

# The parent dir of the current file that will be used to create all following folders
# in which results will be stored
parent_dir=$(dirname $(pwd))

# The date is used to version the experiemntations and to know which experimentation
# has been done on which day
date_str=$(date +"%d-%m-%Y")
#date_str="07-11-2024"

# The relative path for storing experiments data
category="128/linear/3nodes/linear"

# This is to give an indication to the script from where the script is executed
# From the home environment or from the Grid
#root_prefix="/home/erods-chouette/Documents/"
#init_root_prefix="/home/erods-chouette/"

#Production environment
init_root_prefix="/home/ykoagnenzali/"
root_prefix="/home/ykoagnenzali/"

prefix_folder="${root_prefix}synchronizeExperimentation"

#Those paths are given to a indicate to the script that fecth data, where the metrics for istio are
# created and also the 
istio_path="../istio_metrics.json"
metric_path="../teastore_grenoble.json"

# This is the adress of the server where your applciation is deployed plus the 
# frontend page you want to access
host="$WEBUI"

# The kubernetes credentials to used for entering the cluster
#export KUBECONFIG=~/admin_collect-data.conf
export KUBECONFIG="${init_root_prefix}admin_load3.conf"

# This script deployed every necessary configuration for istio mesh
/bin/bash "$prefix_folder/mesh/istio.sh" $prefix_folder

  #number=$((number + 1))
  #new_folder_path="${new_folder_path1}/${number}"
  for element in train_load_50
    do
      # Complete relative path for data storage
      new_folder_base="$parent_dir/synchronizeExperimentation/locust/$site/train/$date_str/${element}$PATH_SUFFIX/hyperthreading"
      #new_folder_base="$parent_dir/synchronizeExperimentation/locust/train/$element/nantes/hyperthreading/$category/$date_str"
      new_folder_path1="$new_folder_base"
      new_folder_path_backup="$new_folder_base/backup"

      kubectl create -f $prefix_folder/benchmarks/train-ticket/ts-deployment-part1.yml
      sleep 120
      kubectl create -f $prefix_folder/benchmarks/train-ticket/ts-deployment-part2.yml
      kubectl create -f $prefix_folder/benchmarks/train-ticket/ts-deployment-part3.yml
      # kubectl apply  -f trainticket-gateway.yaml
      sleep 480
      python3 $prefix_folder/workload_generators/locust/ts_api_invoke_test.py $host

      #env INTENSITY_FILE="$prefix_folder$WARMUP_FILE" locust -f $prefix_folder/workload_generators/locust/teastore_locustfile-custom-scale.py --headless --host $host
      #env INTENSITY_FILE="$prefix_folder$WARMUP_FILE" locust -f $prefix_folder/workload_generators/locust/bi_locustfile_request.py --headless --csv $log_exp_folder_path --host $host

     # sleep 120

      for file_name in $prefix_folder/Load/$element/*.csv;
        do
            for i in $(seq 1 8);
              do
                root_file_name=$(basename "$file_name" .csv)

                # Compter le nombre de fichiers dans le répertoire $date_str
                file_count=$(ls -1 "$new_folder_path1" | wc -l)

                # Créer le sous-répertoire "experimentation" avec le numéro
                exp_folder_path="$new_folder_path1/$root_file_name"
                log_exp_folder_path="${new_folder_path1}/output/${root_file_name}_$i"

                echo $root_file_name

                input_string=$file_name
                output_part=$(basename "$input_string" .csv)
                output_part="${output_part#profiles_}"

                echo "##################### Sleeping before load ##################################################"

                result="$output_part.csv"

                time_obj=$(date +"%H:%M:%S")
                echo $time_obj


                #env INTENSITY_FILE=$file_name locust -f ./request_type/bi_locustfile_request.py --headless --csv=log --csv-full-history
                env INTENSITY_FILE="$file_name" locust -f $prefix_folder/workload_generators/locust/bi_locustfile_request.py --headless --csv $log_exp_folder_path --host $host

                sleep 60

                python3 $prefix_folder/Fetcher/fetch_organized_for_mean.py "$result" "$workload_dir" "$exp_folder_path" "$time_obj" "$PROMETHEUS_URL" "$DURATION" "$prefix_folder"
                python3 $prefix_folder/Fetcher/istio_metric_fetch.py "$new_folder_path1" "$time_obj" "$istio_path" "$PROMETHEUS_URL" "$DURATION" "$root_file_name"
                #python3 $prefix_folder/Fetcher/istio_metric_fetch_backup.py "$new_folder_path_backup" "$time_obj" $metric_path $istio_path $root_file_name

          done
      done
        kubectl delete -f $prefix_folder/benchmarks/train-ticket/ts-deployment-part1.yml
        kubectl delete -f $prefix_folder/benchmarks/train-ticket/ts-deployment-part2.yml
        kubectl delete -f $prefix_folder/benchmarks/train-ticket/ts-deployment-part3.yml
    done
