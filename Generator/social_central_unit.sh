#!/bin/bash

export PATH="$HOME/.local/bin:$PATH"

# Obtenir le répertoire parent
parent_dir=$(dirname $(pwd))

# Obtenir la date actuelle
date_str=$(date +"%d-%m-%Y")

category="128/linear/3nodes/linear"

# Chemin complet du nouveau dossier
new_folder_path="$parent_dir/locust/social/nantes/hyperthreading/$category/$date_str"


workload_date=$(date +"%Y-%m-%d")
#workload_dir="../Load/profiles_$workload_date"
workload_dir="../Load/profiles_2024-07-31"


workload_files=($(ls "$workload_dir"/*.csv))

export KUBECONFIG=~/admin_k8s_social.conf
#export KUBECONFIG=~/socialNetwork/admin_k8s_chouette.conf


for file_name in ../Load/socialnetwork_loads/*.csv; do

# Compter le nombre de fichiers dans le répertoire $date_str
file_count=$(ls -1 "$new_folder_path" | wc -l)

# Créer le sous-répertoire "experimentation" avec le numéro
exp_folder_path="$new_folder_path/experimentation$((file_count + 1))"

echo $file_name

input_string=$file_name
output_part=$(basename "$input_string" .csv)
output_part="${output_part#profiles_}"
echo "$output_part"

echo "##################### Initialisation ##################################################"

# Créer le déploiement Kubernetes
helm install socialnetwork ../benchmarks/DeathStarBench/socialNetwork/helm-chart/socialnetwork/
kubectl rollout status deployment nginx-thrift
kubectl apply -f ../socialNetwork/nginx-thrift-nodeport.yaml
kubectl apply -f ../socialNetwork/media-frontend-nodeport.yaml
#
sleep 180

echo "##################### Sleeping before warmup ##################################################"

warm="../warmUp/const_linear_30requests_per_sec.csv"

#for warmp in ../warmUp/*.csv; do
#Lancer le générateur de charge HTTP
#env INTENSITY_FILE=$warm locust -f ~/PycharmProjects/synchronizeExperimentation/workload_generators/locust/teastore_locustfile-custom-scale.py --headless --csv=log --csv-full-history

python3 ../workload_generators/locust/warmup.py --graph ../workload_generators/locust/datasets/social-graph/socfb-Reed98.mtx --addr http://econome-20.nantes.grid5000.fr:30081

sleep 120

echo "##################### Sleeping before load ##################################################"

result="$output_part.csv"

#time_obj=$(date +"%H:%M:%S.%3N")
time_obj=$(date +"%H:%M:%S")

media_addr="http://econome-20.nantes.grid5000.fr:30082"
webui_addr="http://econome-20.nantes.grid5000.fr:30081"

REQUEST="mixed"

env NGINX_ADDR=$webui_addr MEDIA_ADDR=$media_addr INTENSITY_FILE=$file_name COMP_OPT=$REQUEST locust -f ../workload_generators/locust/locustfile-custom-scale.py --headless --csv=log --csv-full-history

python3 ../Fetcher/locustPostFetcher2.py "$result" $workload_dir $exp_folder_path $time_obj
python3 ../Fetcher/testavance2.py $exp_folder_path $time_obj

#kubectl delete pods,deployments,services -l app=teastore
helm uninstall socialnetwork
sleep 120

done