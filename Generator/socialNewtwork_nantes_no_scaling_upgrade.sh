#!/bin/bash
#python3 locust/warmup.py --graph ./datasets/social-graph/socfb-Reed98.mtx --addr http://172.16.192.9:30081

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
new_folder_path="$parent_dir/socialNetwork/locust/nantes/hyperthreading/$category/$date_str"

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
workload_dir="../Load/profiles_2024-09-18"
warmup_dir="../warmUp"

pwd

workload_files=($(ls "$workload_dir"/*.csv))


warmup="const_linear_80requests_per_sec.csv"

warmupFile="../warmUp/${warmup}"

echo $warmupFile

export KUBECONFIG=~/admin_k8s_chouette.conf

#for file_name in "${workload_files[@]}"; do
# shellcheck disable=SC2066
for file_name in ../Load/profiles_2024-07-31/*.csv; do

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

warm="warmup-$output_part.csv"

#python3 warmup.py --graph ./datasets/social-graph/socfb-Reed98.mtx --addr http://172.16.192.9:30081

#for warmp in ../warmUp/*.csv; do
#Lancer le générateur de charge HTTP
#env INTENSITY_FILE=$warmp locust -f ~/Experimentations/synchronizeExperimentation/workload_generators/locust/teastore_locustfile-custom-scale.py --headless --csv=log --csv-full-history

#done
#sleep 180

#echo "##################### Sleeping before autoscaler ##################################################"


echo "##################### Sleeping before load ##################################################"

#sleep 120

#result="$output_part.csv"
result="output-$output_part.csv"

res="$output_part.csv"
media_addr="http://172.16.192.9:30082"
webui_addr="http://172.16.192.9:30081"
REQUEST="composePost"

time_obj=$(date +"%H:%M:%S.%3N")

echo "le fichier de profil"
echo $file_name

env NGINX_ADDR=$webui_addr MEDIA_ADDR=$media_addr INTENSITY_FILE=$file_name COMP_OPT=$REQUEST locust -f ../workload_generators/locust/locustfile-custom-scale.py --headless --csv=log --csv-full-history

#java -jar httploadgenerator.jar director -s $target -a "$file_name" -l "./teastore_buy.lua" -o "$result" -t $nb_thread

echo "#########################Load Injection finished######################################"

sleep 120

#moveRepo="../Load/intensity_profiles_2024-07-14/"

python3 ../Fetcher/socialFecther.py "$result" $workload_dir $exp_folder_path $time_obj
#python3 ../Fetcher/PostFetcher.py $warm $warmup_dir $exp_folder_path

#sleep 60

#mv ../Load/intensity_profiles_2024-07-14/$result $lOutput
#mv "$workload_dir/$result" $lOutput

#kubectl delete pods,deployments,services -l app=teastore

sleep 240

done