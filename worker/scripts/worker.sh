#!/bin/bash

#git pull

echo "Script parameter: $1"

echo "worker $1"
# Adresse SSH du serveur worker
WORKER_SSH_HOST=$1

# Nom de la screen où le worker est lancé
WORKER_SCREEN_NAME="worker"

# Chemin complet du dossier contenant le worker
# shellcheck disable=SC2088
WORKER_DIR="~/Experimentations/synchronizeExperimentation/worker"
#WORKER_DIR="~/synchronizeExperimentation/worker"

# Commande pour lancer le worker
WORKER_COMMAND="java -jar -Xms16g -Xmx32g -Xss256k ./httploadgenerator.jar loadgenerator"

echo "on lance la connexyoon"
# Connexion SSH au serveur worker
# shellcheck disable=SC2087
ssh "$WORKER_SSH_HOST" << EOF
  # Arrêt de la screen existante
  screen -S $WORKER_SCREEN_NAME -X quit

  sleep 20
  # Création d'une nouvelle screen et lancement du worker
  cd $WORKER_DIR
  #screen -wipe

  screen -S $WORKER_SCREEN_NAME -d -m $WORKER_COMMAND
EOF

echo "on a fini"