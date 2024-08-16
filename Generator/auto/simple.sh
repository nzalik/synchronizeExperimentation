#!/bin/bash

pwd
echo "le path dedepart"
echo "$PATH"

NODE_SSH_HOST=$1

#WORKER_DIR="/home/ykoagnenzali/Experimentations/synchronizeExperimentation/"
# shellcheck disable=SC2088
WORKER_DIR="~/Experimentations/synchronizeExperimentation/worker"

echo "Script deployment with : $1"

DEPLOY_SCREEN_NAME="deployment"

WORKER_COMMAND="java -jar -Xms16g -Xmx32g -Xss256k ./httploadgenerator.jar loadgenerator"

#WORKER_COMMAND="export PATH=\"\$HOME/.local/bin:\$PATH\"; export KUBECONFIG=/home/admin.conf; kubectl get nodes"

# shellcheck disable=SC2087
ssh "$NODE_SSH_HOST" << EOF
  # Arrêt de la screen existante
  screen -S $DEPLOY_SCREEN_NAME -X quit

  # Création d'une nouvelle screen et lancement du worker
  cd $WORKER_DIR
  screen -S $DEPLOY_SCREEN_NAME -d -m $WORKER_COMMAND
EOF
