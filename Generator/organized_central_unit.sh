#!/bin/bash

export PATH="$HOME/.local/bin:$PATH"

# Obtenir le répertoire parent
parent_dir=$(dirname $(pwd))

# Obtenir la date actuelle
date_str=$(date +"%d-%m-%Y")

category="128/linear/3nodes/linear"

# Chemin complet du nouveau dossier
new_folder_path1="$parent_dir/locust/weekend/nantes/hyperthreading/$category/$date_str"

istio_path="../istio_metrics.json"
metric_path="../teastore_grenoble.json"

workload_date=$(date +"%Y-%m-%d")
#workload_dir="../Load/profiles_$workload_date"
workload_dir="../Load/profiles_2024-07-31"

host="http://econome-20.nantes.grid5000.fr:30080/tools.descartes.teastore.webui"

workload_files=($(ls "$workload_dir"/*.csv))

export KUBECONFIG=~/admin_collect-data.conf

  #/bin/bash "$parent_dir/mesh/istio.sh"

  #kubectl create secret docker-registry docker-registry-secret --docker-server=https://gricad-registry.univ-grenoble-alpes.fr --docker-username=chouette --docker-password=esVsrrxsLA9sJ_nzPurJ

  #number=$((number + 1))
  #new_folder_path="${new_folder_path1}/${number}"
  for file_name in ../Load/load2/*.csv; do
  for i in {1..4}; do
  root_file_name=$(basename "$file_name" .csv)

  # Compter le nombre de fichiers dans le répertoire $date_str
  file_count=$(ls -1 "$new_folder_path1" | wc -l)

  echo "le nombre de fichier"
  echo $file_count

  # Créer le sous-répertoire "experimentation" avec le numéro
  exp_folder_path="$new_folder_path1/$root_file_name"
  log_exp_folder_path="${new_folder_path1}/output/${root_file_name}"

  echo $root_file_name

  input_string=$file_name
  output_part=$(basename "$input_string" .csv)
  output_part="${output_part#profiles_}"
  echo "$output_part"

  echo "##################### Initialisation ##################################################"

  # Créer le déploiement Kubernetes
  kubectl create -f ../custom_deployments/gricard-teastore.yaml
  #kubectl create -f ../custom_deployments/teastore-clusterip-1cpu-5giga.yaml

  sleep 240

  echo "##################### Sleeping befor240e warmup ##################################################"

  warm="../warmUp/const_linear_30requests_per_sec.csv"

  #for warmp in ../warmUp/*.csv; do
  #Lancer le générateur de charge HTTP
  #env INTENSITY_FILE=$warm locust -f ~/PycharmProjects/synchronizeExperimentation/workload_generators/locust/teastore_locustfile-custom-scale.py --headless --csv=log --csv-full-history
  env INTENSITY_FILE=$warm locust -f /home/erods-chouette/Documents/synchronizeExperimentation/workload_generators/locust/teastore_locustfile-custom-scale.py --headless --host $host

  sleep 120

  echo "##################### Sleeping before load ##################################################"

  result="$output_part.csv"

  time_obj=$(date +"%H:%M:%S")
  echo $time_obj

  env INTENSITY_FILE=$file_name locust -f /home/erods-chouette/Documents/synchronizeExperimentation/workload_generators/locust/teastore_locustfile-custom-scale.py --headless --csv $log_exp_folder_path --host $host

  sleep 60

  python3 ../Fetcher/fetch_organized_for_mean.py "$result" $workload_dir $exp_folder_path $time_obj $metric_path
  python3 ../Fetcher/istio_metric_fetch.py "$new_folder_path1" "$time_obj" $metric_path $istio_path $root_file_name

  kubectl delete pods,deployments,services -l app=teastore

  sleep 120

  done
done