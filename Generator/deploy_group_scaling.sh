#!/bin/bash

NODE_SSH_HOST=$1

WORKER_DIR="/home/ykoagnenzali/Experimentations/synchronizeExperimentation/"

echo "Script deployment with : $1"

# shellcheck disable=SC2087
ssh "$NODE_SSH_HOST" << EOF
set -e  # Arrête le script en cas d'erreur

sudo-g5k apt update

# Téléchargement de kubectl
curl -LO "https://dl.k8s.io/release/\$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl
mv ./kubectl /usr/local/bin/kubectl

# Vérification de la version kubectl
kubectl version --client

# Affichage du PATH pour diagnostic
echo \$PATH

# Cible et variable de répertoire
target=\$2
echo "target=\$target"
echo "WORKER_DIR=\$WORKER_DIR"

# Mise à jour Git
git pull

# Navigation dans le répertoire de travail
cd \$WORKER_DIR || exit
pwd

# Configuration KUBECONFIG
export KUBECONFIG=/home/ykoagnenzali/admin.conf

# Exécution de commandes kubectl
kubectl get nodes > nodes.txt
kubectl create -f custom_deployments/teastore-clusterip-1cpu-5giga.yaml > deploy.txt
kubectl get pods > pods.txt

EOF