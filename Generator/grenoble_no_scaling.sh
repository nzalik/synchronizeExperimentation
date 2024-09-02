#!/bin/bash

export PATH="$HOME/.local/bin:$PATH"

#Node reservation and worker start
target=$(python3 ./worker_startup.py grenoble dahu)

sleep 60

echo "************** The worker is okay ***************"
echo "lancé sur le $target"

#Initialise the target

nb_thread=128

# Obtenir le répertoire parent
parent_dir=$(dirname $(pwd))

# Obtenir la date actuelle
date_str=$(date +"%d-%m-%Y")

category="128/group/3nodes/linear"

# Chemin complet du nouveau dossier
new_folder_path="$parent_dir/grenoble/hyperthreading/$category/$date_str"

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


#wOutput="$exp_folder_path/warmup"
lOutput="$exp_folder_path/data/load"

#if [ ! -d "$wOutput" ]; then
#    mkdir -p "$wOutput"
#fi

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
#workload_dir="../Load/profiles_$workload_date"
workload_dir="../Load/profiles_2024-07-31"
warmup_dir="../warmUp"

pwd

workload_files=($(ls "$workload_dir"/*.csv))


warmup="const_linear_80requests_per_sec.csv"

warmupFile="../warmUp/${warmup}"

echo $warmupFile

export KUBECONFIG=/home/ykoagnenzali/admin_chouette-scale.conf

#for file_name in workload_files:
for file_name in "${workload_files[@]}"; do

python3 ./worker_restart.py "$target"

sleep 60

echo $file_name

input_string=$file_name
output_part=$(basename "$input_string" .csv)
output_part="${output_part#profiles_}"
echo "$output_part"

echo "##################### Initialisation ##################################################"

# Créer le déploiement Kubernetes
kubectl create -f ../custom_deployments/teastore-clusterip-1cpu-5giga.yaml

sleep 300

echo "##################### Sleeping before warmup ##################################################"

warm="warmup-$output_part.csv"

#Lancer le générateur de charge HTTP
java -jar httploadgenerator.jar director -s $target -a "$warmupFile" -l "./teastore_buy.lua" -o "$warm" -t $nb_thread

#sleep 180

#echo "##################### Sleeping before autoscaler ##################################################"


echo "##################### Sleeping before load ##################################################"

sleep 240

#result="$output_part.csv"
result="output-$output_part.csv"

res="$output_part.csv"


java -jar httploadgenerator.jar director -s $target -a "$file_name" -l "./teastore_buy.lua" -o "$result" -t $nb_thread

echo "#########################Load Injection finished######################################"

sleep 60

#moveRepo="../Load/intensity_profiles_2024-07-14/"

# shellcheck disable=SC2086
python3 ../Fetcher/PostFetcher.py "$result" $workload_dir $exp_folder_path
#python3 ../Fetcher/PostFetcher.py $warm $warmup_dir $exp_folder_path

sleep 60

#mv ../Load/intensity_profiles_2024-07-14/$result $lOutput
mv "$workload_dir/$result" $lOutput

kubectl delete pods,deployments,services -l app=teastore

sleep 240

done