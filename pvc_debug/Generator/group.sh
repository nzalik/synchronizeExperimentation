#!/bin/bash

run_first_command() {
  ehco "Start injection"
  java -jar httploadgenerator.jar director -s localhost -a "$file" -l "./teastore_buy.lua" -o "output-$file_name-restart-from-cluster2-10min-100req.csv" -t 256
}

# Fonction pour exécuter la deuxième commande
run_second_command() {

  kopf run ../hooks_horizontal.py -n default --dev
}

# Liste des fichiers de charge
workload_files=(
  "intensity_profile-three-21-06-2024-10min-100.0requests.csv"
)

workload_files_prefix="/home/erods-chouette/PycharmProjects/collectMetrics/Workloads/intensity_profile-three-28-06-2024-10min-130.0requests.csv"

prefix="/home/erods-chouette/PycharmProjects/collectMetrics"

 pwd

 export KUBECONFIG=/home/erods-chouette/admin.conf

warmup="intensity_profile-three-26-06-2024-3min-10.0requests.csv"

for file_name in "${workload_files[@]}"; do
  echo "##################### Start cleaning the app ##################################################"


  #kubectl delete pods,deployments,services -l app=teastore

  echo "##################### Good bye cleaning ##################################################"

  echo "##################### Sleep for ten minutes ##################################################"

  #sleep 300


  warmupFile="${prefix}/Workloads/${warmup}"
  file="${workload_files_prefix}"

  echo "##################### Initialisation ##################################################"


  # Créer le déploiement Kubernetes
  kubectl create -f /home/erods-chouette/Documents/RESEARCH/BENCHMARK/Experimentations/TeaStore/examples/kubernetes/custom_deployments/teastore-clusterip-1cpu-5giga.yaml

  sleep 180

  #kubectl create -f "$prefix/autoscalers/autoscaler-nodb-noregistry-5-max-replicas.yaml"
  #kubectl create -f "$prefix/autoscalers/metrics_server.yaml"

  #sleep 60

  # Lancer le générateur de charge HTTP
  java -jar httploadgenerator.jar director -s localhost -a "$warmupFile" -l "./teastore_buy.lua" -o "warmup-$file_name-3min.csv" -t 256

 # echo "****************warmup end *******************************"
  sleep 240

  (run_first_command) &

  sleep 300

  (run_second_command) &

  echo "##################### Started group ##################################################"

done
