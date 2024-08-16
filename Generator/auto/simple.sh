#!/bin/bash

pwd
echo "le path dedepart"
echo "$PATH"

NODE_SSH_HOST=$1

WORKER_DIR="/home/ykoagnenzali/Experimentations/synchronizeExperimentation/"

echo "Script deployment with : $1"

# shellcheck disable=SC2087
ssh "$NODE_SSH_HOST" << 'EOSSH'
set -e  # Arrête le script en cas d'erreur

# Créer une nouvelle session screen détachée
screen -dmS my_session bash -c '
    set -e  # Arrête le script en cas d'erreur

    # Ajouter le répertoire .local/bin au PATH
    export PATH="$HOME/.local/bin:$PATH"

    echo "le path sur le noeud"
    echo $PATH

    # Mise à jour Git
    git pull

    pwd

    # Configuration KUBECONFIG
    export KUBECONFIG=/home/ykoagnenzali/admin.conf

    # Exécution de commandes kubectl
    kubectl get nodes > nodes.txt
    kubectl create -f custom_deployments/teastore-clusterip-1cpu-5giga.yaml > deploy.txt
    kubectl get pods > pods.txt
'

# Fin de la session SSH
EOSSH