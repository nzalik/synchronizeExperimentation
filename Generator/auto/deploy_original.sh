#!/bin/bash

echo "target $2"
echo "deployment $1"

NODE_SSH_HOST=$1

target=$2

nb_thread=128

# Obtenir le répertoire parent
parent_dir=$(dirname $(pwd))

# Obtenir la date actuelle
date_str=$(date +"%d-%m-%Y")

category="128/group/3nodes/linear"

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

# shellcheck disable=SC2088
WORKER_DIR="~/Experimentations/synchronizeExperimentation"

workload_date=$(date +"%Y-%m-%d")
#workload_dir="../Load/profiles_$workload_date"
workload_dir="../Load/profiles_2024-07-31"

warmup_dir="./warmUp"

workload_files=($(ls "$workload_dir"/*.csv))

warmup="const_linear_80requests_per_sec.csv"

warmupFile="../warmUp/${warmup}"

# shellcheck disable=SC2087
ssh -tt "$NODE_SSH_HOST" << EOF

  cd $WORKER_DIR

  pwd
  ls ./

  export PATH="$HOME/.local/bin:$PATH"
  export KUBECONFIG=/home/ykoagnenzali/admin.conf

  for file_name in "${workload_files[@]}"; do
  echo $file_name
  done

EOF