#!/bin/bash

export PATH="$HOME/.local/bin:$PATH"

# Obtenir le répertoire parent
parent_dir=$(dirname $(pwd))

# Obtenir la date actuelle
date_str=$(date +"%d-%m-%Y")

category="128/linear/3nodes/linear"

# Chemin complet du nouveau dossier
new_folder_path="$parent_dir/locust/advanced/nantes/hyperthreading/$category/$date_str"


workload_date=$(date +"%Y-%m-%d")
#workload_dir="../Load/profiles_$workload_date"
workload_dir="../Load/profiles_2024-07-31"


workload_files=($(ls "$workload_dir"/*.csv))


export KUBECONFIG=~/admin_k8s_teastore.conf


for file_name in ../Load/teastore_loads/*.csv; do

# Compter le nombre de fichiers dans le répertoire $date_str
file_count=$(ls -1 "$new_folder_path" | wc -l)

echo "le nombre de fichier"
echo $file_count

# Créer le sous-répertoire "experimentation" avec le numéro
exp_folder_path="$new_folder_path/experimentation$((file_count + 1))"

echo $file_name

input_string=$file_name
output_part=$(basename "$input_string" .csv)
output_part="${output_part#profiles_}"
echo "$output_part"

echo "##################### Initialisation ##################################################"

# Créer le déploiement Kubernetes
kubectl create -f ../custom_deployments/gricard-teastore.yaml
#kubectl create -f ../custom_deployments/teastore-clusterip-1cpu-5giga.yaml

sleep 240

echo "##################### Sleeping before warmup ##################################################"

warm="../warmUp/const_linear_30requests_per_sec.csv"

#for warmp in ../warmUp/*.csv; do
#Lancer le générateur de charge HTTP
env INTENSITY_FILE=$warm locust -f ~/synchronizeExperimentation/workload_generators/locust/teastore_locustfile-custom-scale.py --headless --csv=log --csv-full-history

sleep 120

echo "##################### Sleeping before load ##################################################"

result="$output_part.csv"

time_obj=$(date +"%H:%M:%S")
echo $time_obj

env INTENSITY_FILE=$file_name locust -f ~/synchronizeExperimentation/workload_generators/locust/teastore_locustfile-custom-scale.py --headless --csv=log --csv-full-history


python3 ../Fetcher/locustPostFetcher.py "$result" $workload_dir $exp_folder_path $time_obj
python3 ../Fetcher/testavance.py $exp_folder_path $time_obj

kubectl delete pods,deployments,services -l app=teastore

sleep 180

done