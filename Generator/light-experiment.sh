#!/bin/bash

#

# Liste des fichiers de charge
workload_files=(
  "intensity_profile-three-27-06-2024-10min-160.0requests.csv"
)

workload_files_prefix="/home/erods-chouette/PycharmProjects/collectMetrics/Workloads/"
prefix="/home/erods-chouette/PycharmProjects/collectMetrics/"

warmup="intensity_profile-three-26-06-2024-3min-10.0requests.csv"

for file_name in "${workload_files[@]}"; do
  warmupFile="${workload_files_prefix}${warmup}"
  file="${workload_files_prefix}${file_name}"

  echo "Warmup"
  echo "$warmupFile"

  echo "Lancement"
  echo "$file"


  pwd

  #export KUBECONFIG=/home/erods-chouette/admin.conf

  # Créer le déploiement Kubernetes
  #kubectl create -f /home/erods-chouette/Documents/RESEARCH/BENCHMARK/Experimentations/TeaStore/examples/kubernetes/custom_deployments/teastore-clusterip-1cpu-5giga.yaml

  #echo "Sleeping"
  #sleep 600
  #kubectl create -f "$prefix/autoscalers/autoscaler-nodb-noregistry-5-max-replicas.yaml"
  #kubectl create -f "$prefix/autoscalers/metrics_server.yaml"

  #sleep 60

  # Lancer le générateur de charge HTTP
  #java -jar httploadgenerator.jar director -s localhost -a "$warmupFile" -l "$prefix/Generator/teastore_buy.lua" -o "warmup-$file_name-3min.csv" -t 10

 # echo "****************warmup end *******************************"
  #sleep 180

  java -jar httploadgenerator.jar director -s localhost -a "$file" -l "$prefix/Generator/teastore_buy.lua" -o "output-$file_name-restart.csv" -t 256
  echo "#########################Load Injection finished######################################"
  #sleep 180

  #kubectl delete pods,deployments,services -l app=teastore
  #sleep 300
done