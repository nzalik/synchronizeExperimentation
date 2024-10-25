#!/bin/bash

sleep 60
# Liste des fichiers de charge
# shellcheck disable=SC2054
workload_files=(
   "intensity_profile-three-21-06-2024-10min-100.0requests.csv",
)

workload_dir="../load"

#workload_files=($(ls "$workload_dir"/*.csv))

warmup="intensity_profile-three-26-06-2024-3min-10.0requests.csv"

warmupFile="../warmUp/${warmup}"

echo $warmupFile



export KUBECONFIG=/home/erods-chouette/admin.conf

#for file_name in workload_files:
for file_name in "${workload_files[@]}"; do

file="../Load/intensity_profiles_2024-07-11_14-43-04/intensity_profile_10requests_per_sec.csv"


echo "##################### Start cleaning the app ##################################################"

#kubectl delete pods,deployments,services -l app=teastore

echo "##################### Good bye cleaning ##################################################"

echo "##################### Sleep for ten minutes ##################################################"

#sleep 240


#echo "##################### Initialisation ##################################################"

  # Créer le déploiement Kubernetes
#kubectl create -f ../custom_deployments/teastore-clusterip-1cpu-5giga.yaml

#sleep 300

#echo "##################### Sleeping before warmup ##################################################"
#
## Lancer le générateur de charge HTTP
#java -jar httploadgenerator.jar director -s localhost -a "$warmupFile" -l "./teastore_buy.lua" -o "warmup-$file_name-3min.csv" -t 256
#
#echo "##################### Sleeping before load ##################################################"
#
#sleep 240
#
result="output-$file_name-restart-cluster1.csv"
#
java -jar httploadgenerator.jar director -s localhost -a "$file" -l "./teastore_buy.lua" -o $result -t 256
#
echo "#########################Load Injection finished######################################"
#
sleep 160

python3 ../Fecther_without_threshold/PostFectherUpdateVersion.py $result

sleep 160

kubectl delete pods,deployments,services -l app=teastore

sleep 300

done