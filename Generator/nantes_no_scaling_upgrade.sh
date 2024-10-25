#!/bin/bash

export PATH="$HOME/.local/bin:$PATH"

#Node reservation and worker start
#target=$(python3 ./worker_startup.py nantes econome)

#sleep 60

echo "************** The worker is okay ***************"
#echo "lancé sur le $target"

#Initialise the target

nb_thread=128

# Obtenir le répertoire parent
parent_dir=$(dirname $(pwd))

# Obtenir la date actuelle
date_str=$(date +"%d-%m-%Y")

category="128/group/3nodes/linear"

# Chemin complet du nouveau dossier
new_folder_path="$parent_dir/locust/advanced/nantes/hyperthreading/$category/$date_str"


# Compter le nombre de fichiers dans le répertoire $date_str
file_count=$(ls -1 "$new_folder_path" | wc -l)

# Créer le sous-répertoire "experimentation" avec le numéro
exp_folder_path="$new_folder_path/experimentation$((file_count + 1))"


#sleep 60
# Liste des fichiers de charge
# shellcheck disable=SC2054
#workload_files=(
#   "intensity_profile-three-21-06-2024-10min-100.0requests.csv",
#)
workload_date=$(date +"%Y-%m-%d")
#workload_dir="../Load/profiles_$workload_date"
workload_dir="../Load/profiles_2024-07-31"

pwd

workload_files=($(ls "$workload_dir"/*.csv))


warmup="const_linear_80requests_per_sec.csv"

warmupFile="../warmUp/${warmup}"

echo $warmupFile

export KUBECONFIG=~/admin_k8s_chouette.conf

#for file_name in "${workload_files[@]}"; do
# shellcheck disable=SC2066
for file_name in ../Load/profiles_2024-09-18/*.csv; do

#python3 ./worker_restart.py "$target"

#sleep 60

echo $file_name

input_string=$file_name
output_part=$(basename "$input_string" .csv)
output_part="${output_part#profiles_}"
echo "$output_part"

echo "##################### Initialisation ##################################################"

# Créer le déploiement Kubernetes
#kubectl create -f ../custom_deployments/gricard-teastore.yaml
#kubectl create -f ../custom_deployments/teastore-clusterip-1cpu-5giga.yaml

#sleep 240

echo "##################### Sleeping before warmup ##################################################"

warm="../warmUp/const_linear_30requests_per_sec.csv"

#for warmp in ../warmUp/*.csv; do
#Lancer le générateur de charge HTTP
#env INTENSITY_FILE=$warm locust -f ~/PycharmProjects/synchronizeExperimentation/workload_generators/locust/teastore_locustfile-custom-scale.py --headless --csv=log --csv-full-history

#done
#sleep 180

#echo "##################### Sleeping before autoscaler ##################################################"


echo "##################### Sleeping before load ##################################################"

#sleep 120

result="$output_part.csv"
#result="output-$output_part.csv"

#res="$output_part.csv"

time_obj=$(date +"%H:%M:%S.%3N")

env INTENSITY_FILE=$file_name locust -f ~/PycharmProjects/synchronizeExperimentation/workload_generators/locust/teastore_locustfile-custom-scale.py --headless --csv=log --csv-full-history

#java -jar httploadgenerator.jar director -s $target -a "$file_name" -l "./teastore_buy.lua" -o "$result" -t $nb_thread

#echo "#########################Load Injection finished######################################"

#sleep 120

#moveRepo="../Load/intensity_profiles_2024-07-14/"

python3 ../Fetcher/locustPostFetcher.py "$result" $workload_dir $exp_folder_path $time_obj

#python3 ../Fetcher/PostFetcher.py $warm $warmup_dir $exp_folder_path
#fetch_d="../metric-dataset-generator/metric_fetcher"
#prometheus_url="http://172.16.192.6:32170"
#data_dir="../routes/"
#duration="3"
#time_step="1"
#namespace="default"

#python3 ../Fetcher/socialFecther.py "$result" $workload_dir $exp_folder_path $time_obj
#python3 ../metric-dataset-generator/metric_fetcher/prometheus_fetch.py "$result" $workload_dir $exp_folder_path $time_obj

#python3 $fetch_d/prometheus_fetch.py $prometheus_url \
#				-N "teastore" -d "$data_dir" -p "node_dist_1/hw_spec_2/pod_spec_0/$REQUEST/$INTENSITY/" \
#				-t $duration -s $time_step -c $fetch_d/metrics.ini -n $namespace
#sleep 60

done