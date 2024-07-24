#!/bin/bash

export PATH="$HOME/.local/bin:$PATH"

target="172.16.192.18"

nb_thread=256
# Obtenir le répertoire parent
parent_dir=$(dirname $(pwd))

# Obtenir la date actuelle
date_str=$(date +"%d-%m-%Y")

# Chemin complet du nouveau dossier
new_folder_path="$parent_dir/nantes/hyperthreading/$date_str"

# Créer le nouveau dossier s'il n'existe pas déjà
if [ ! -d "$new_folder_path" ]; then
    mkdir "$new_folder_path"
fi

wOutput="$new_folder_path/warmUpOutput"
lOutput="$new_folder_path/LoadOutput"

if [ ! -d "$wOutput" ]; then
    mkdir -p "$wOutput"
fi

if [ ! -d "$lOutput" ]; then
    mkdir -p "$lOutput"
fi

#sleep 60
# Liste des fichiers de charge
# shellcheck disable=SC2054
#workload_files=(
#   "intensity_profile-three-21-06-2024-10min-100.0requests.csv",
#)
workload_date=$(date +"%Y-%m-%d")
workload_dir="../Load/profiles_$workload_date"

pwd



workload_files=($(ls "$workload_dir"/*.csv))


warmup="const_linear_80requests_per_sec.csv"

warmupFile="../warmUp/${warmup}"

echo $warmupFile

export KUBECONFIG=/home/ykoagnenzali/admin.conf

#for file_name in workload_files:
for file_name in "${workload_files[@]}"; do

echo $file_name

input_string=$file_name
output_part=$(basename "$input_string" .csv)
output_part="${output_part#profiles_}"
echo "$output_part"

echo "##################### Initialisation ##################################################"

# Créer le déploiement Kubernetes
#kubectl create -f ../custom_deployments/teastore-clusterip-1cpu-5giga.yaml

#sleep 60

#echo "##################### Sleeping before warmup ##################################################"

#Lancer le générateur de charge HTTP
#java -jar httploadgenerator.jar director -s $target -a "$warmupFile" -l "./teastore_buy.lua" -o "warmup-$output_part.csv" -t $nb_thread

#echo "##################### Sleeping before load ##################################################"

#sleep 30

result="$output_part.csv"
#result="output-$output_part.csv"

res="$output_part.csv"


#java -jar httploadgenerator.jar director -s $target -a "$file_name" -l "./teastore_buy.lua" -o $result -t $nb_thread

echo "#########################Load Injection finished######################################"

#sleep 60

#moveRepo="../Load/intensity_profiles_2024-07-14/"

python3 ../Fetcher/PostFetcher.py $res $workload_dir

sleep 60

#mkdir ./load_injector


#mv ../Load/intensity_profiles_2024-07-14/$result $lOutput
#mv ".$workload_dir/$result" $lOutput
mv "$workload_dir/$result" ./load_injector

#kubectl delete pods,deployments,services -l app=teastore

#sleep 600

done