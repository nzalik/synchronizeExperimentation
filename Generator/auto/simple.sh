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

    echo "pas a jour kubeconfig"
    echo $KUBECONFIG

    curl -LO "https://dl.k8s.io/release/\$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x ./kubectl
    sudo-g5k mv ./kubectl /usr/local/bin/kubectl

    # Vérification de la version kubectl
    kubectl version --client

    # Ajouter le répertoire .local/bin au PATH
    export PATH="$PATH:/usr/local/bin"

    echo "le path sur le noeud"
    echo $PATH

    # Mise à jour Git
    git pull

    pwd

    # Configuration KUBECONFIG
    export KUBECONFIG=/home/ykoagnenzali/admin.conf

    echo "le kubeconfig a jour"
    echo $KUBECONFIG
    # Exécution de commandes kubectl
    kubectl get nodes > nodes.txt
    kubectl create -f custom_deployments/teastore-clusterip-1cpu-5giga.yaml > deploy.txt
    kubectl get pods > pods.txt
'

# Fin de la session SSH
EOSSH