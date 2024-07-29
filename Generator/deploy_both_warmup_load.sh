#!/bin/bash

echo "##################### Initialisation1 ##################################################"

export PATH="$HOME/.local/bin:$PATH"

target="172.16.192.8"

nb_thread=128

# Obtenir le répertoire parent
parent_dir=$(dirname $(pwd))

# Obtenir la date actuelle
date_str=$(date +"%d-%m-%Y")

category="128/loadWarmup"

# Chemin complet du nouveau dossier
new_folder_path="$parent_dir/nantes/hyperthreading/$category/$date_str"

# Créer le nouveau dossier s'il n'existe pas déjà
if [ ! -d "$new_folder_path" ]; then
    mkdir -p "$new_folder_path"
fi

# Compter le nombre de fichiers dans le répertoire $date_str
file_count=$(ls -1 "$new_folder_path" | wc -l)

# Créer le sous-répertoire "experimentation" avec le numéro
exp_folder_path="$new_folder_path/experimentation$((file_count + 1))"

if [ ! -d "$exp_folder_path" ]; then
    mkdir -p "$exp_folder_path"
fi


wOutput="$exp_folder_path/warmup"
lOutput="$exp_folder_path/data/load"

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
loadDir="../Load/profiles_2024-07-23"

pwd

workload_files=($(ls "$workload_dir"/*.csv))

load_files=($(ls "$loadDir"/*.csv))


warmup="const_linear_80requests_per_sec.csv"

warmupFile="../warmUp/${warmup}"

#loadFile="../Load/profiles_2024-07-23/linear_200requests_max_per_sec.csv"

echo $warmupFile

export KUBECONFIG=/home/ykoagnenzali/admin.conf

#for file_name in workload_files:
for file_name in "${workload_files[@]}"; do

for element in "${load_files[@]}"; do

echo $file_name
echo "-----------"
echo "$element"

input_string=$file_name
output_part=$(basename "$input_string" .csv)
output_part="${output_part#profiles_}"
echo "$output_part"

elt_string=$element
elt_part=$(basename "$elt_string" .csv)
elt_part="${elt_part#profiles_}"
echo "$elt_part"

echo "##################### Initialisation ##################################################"

# Créer le déploiement Kubernetes
kubectl create -f ../custom_deployments/teastore-clusterip-1cpu-5giga.yaml

sleep 180

#result="$output_part.csv"
result="output-$elt_part.csv"

res="$output_part.csv"

java -jar httploadgenerator.jar director -s $target -a "$file_name" -l "./teastore_buy.lua" -o  "warmup-$output_part.csv" -t $nb_thread

echo "#########################Load Injection finished######################################"

sleep 180

java -jar httploadgenerator.jar director -s $target -a "$element" -l "./teastore_buy.lua" -o $result -t $nb_thread

echo "#########################Load Injection finished######################################"

sleep 60

#moveRepo="../Load/intensity_profiles_2024-07-14/"

saveElement="$exp_folder_path/$output_part"

mkdir -p "$saveElement"

python3 ../Fetcher/fetchWarmup.py $result $loadDir "$saveElement"

sleep 120

mv ../Load/intensity_profiles_2024-07-23/$result $lOutput
#mv "$workload_dir/$result" $lOutput

kubectl delete pods,deployments,services -l app=teastore

sleep 180

done
done