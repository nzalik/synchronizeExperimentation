#!/bin/bash
host="http://econome-20.nantes.grid5000.fr:30080/tools.descartes.teastore.webui"

time_obj=$(date +"%H:%M:%S")
  echo $time_obj
export PATH="$HOME/.local/bin:$PATH"
#kubectl create secret docker-registry docker-registry-secret --docker-server=https://gricad-registry.univ-grenoble-alpes.fr --docker-username=chouette --docker-password=esVsrrxsLA9sJ_nzPurJ
  #number=$((number + 1))
  #new_folder_path="${new_folder_path1}/${number}"
  for file_name in ../Load/load1/*.csv; do
  for i in {1..1}; do

  env INTENSITY_FILE=$file_name locust -f /home/erods-chouette/Documents/synchronizeExperimentation/workload_generators/locust/teastore_locustfile-custom-scale.py --host $host --headless

  done
done