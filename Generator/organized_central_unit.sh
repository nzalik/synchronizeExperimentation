#!/bin/bash

export PATH="$HOME/.local/bin:$PATH"

# The parent dir of the current file that will be used to create all following folders
# in which results will be stored
parent_dir=$(dirname $(pwd))

# The date is used to version the experiemntations and to know which experimentation
# has been done on which day
date_str=$(date +"%d-%m-%Y")


# The relative path for storing experiments data
category="128/linear/3nodes/linear"

# This is to give an indication to the script from where the script is executed
# From the home environment or from the Grid

#prefix_folder="/home/erods-chouette/Documents"
prefix_folder="/home/ykoagnenzali"

# Complete relative path for data storage
new_folder_base="$parent_dir/locust/gab/nantes/hyperthreading/$category/$date_str"
new_folder_path1="$new_folder_base"
new_folder_path_backup="$new_folder_base/backup"

#Those paths are given to a indicate to the script that fecth data, where the metrics for istio are
# created and also the 
istio_path="../istio_metrics.json"
metric_path="../teastore_grenoble.json"

# This is the adress of the server where your applciation is deployed plus the 
# frontend page you want to access
host="http://econome-22.nantes.grid5000.fr:30080/tools.descartes.teastore.webui"

# The kubernetes credentials to used for enterinf the cluster
export KUBECONFIG=~/admin_collect-data.conf

# This script deployed every necessary configuration for istio mesh
/bin/bash "$parent_dir/mesh/istio.sh"

kubectl create secret docker-registry docker-registry-secret --docker-server=https://gricad-registry.univ-grenoble-alpes.fr --docker-username=chouette --docker-password=esVsrrxsLA9sJ_nzPurJ

  #number=$((number + 1))
  #new_folder_path="${new_folder_path1}/${number}"
  for file_name in ../Load/load3/*.csv; do
    for i in {1..2}; do
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

      echo "##################### Initialisation ##################################################"

      # Créer le déploiement Kubernetes
      kubectl create -f ../custom_deployments/gricard-teastore.yaml
      #kubectl create -f ../custom_deployments/teastore-clusterip-1cpu-5giga.yaml

      sleep 240 # This wai time is necessary because the application after being deployed, need some time to
                # be ready to process requests

      echo "##################### Sleeping befor240e warmup ##################################################"

      warm="../warmUp/const_linear_30requests_per_sec.csv"

      #for warmp in ../warmUp/*.csv; do
      #Lancer le générateur de charge HTTP
      #env INTENSITY_FILE=$warm locust -f ~/PycharmProjects/synchronizeExperimentation/workload_generators/locust/teastore_locustfile-custom-scale.py --headless --csv=log --csv-full-history
      env INTENSITY_FILE=$warm locust -f $prefix_folder/synchronizeExperimentation/workload_generators/locust/teastore_locustfile-custom-scale.py --headless --host $host

      sleep 120

      echo "##################### Sleeping before load ##################################################"

      result="$output_part.csv"

      time_obj=$(date +"%H:%M:%S")
      echo $time_obj

      env INTENSITY_FILE=$file_name locust -f $prefix_folder/synchronizeExperimentation/workload_generators/locust/teastore_locustfile-custom-scale.py --headless --csv $log_exp_folder_path --host $host

      sleep 60

      python3 ../Fetcher/fetch_organized_for_mean.py "$result" $workload_dir $exp_folder_path $time_obj $metric_path
      python3 ../Fetcher/istio_metric_fetch.py "$new_folder_path1" "$time_obj" $metric_path $istio_path $root_file_name
      python3 ../Fetcher/istio_metric_fetch_backup.py "$new_folder_path_backup" "$time_obj" $metric_path $istio_path $root_file_name

      kubectl delete pods,deployments,services -l app=teastore

      sleep 120

  done
done