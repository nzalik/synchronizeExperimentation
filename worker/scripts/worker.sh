#!/bin/bash

git pull

# Adresse SSH du serveur worker
WORKER_SSH_HOST="user@worker-server.com"

# Nom de la screen où le worker est lancé
WORKER_SCREEN_NAME="worker"

# Chemin complet du dossier contenant le worker
# shellcheck disable=SC2088
WORKER_DIR="~/Experimentations/synchronizeExperimentation/worker"

# Commande pour lancer le worker
WORKER_COMMAND="java -jar -Xms16g -Xmx32g -Xss256k ./httploadgenerator.jar loadgenerator"

screen -S $WORKER_SCREEN_NAME -X quit

echo "La screen est lance"
  # Création d'une nouvelle screen et lancement du worker
cd $WORKER_DIR
screen -S $WORKER_SCREEN_NAME -d -m $WORKER_COMMAND

echo "le code est lancé"
# Connexion SSH au serveur worker
# shellcheck disable=SC2087
#ssh $WORKER_SSH_HOST << EOF
#  # Arrêt de la screen existante
#  screen -S $WORKER_SCREEN_NAME -X quit
#
#  # Création d'une nouvelle screen et lancement du worker
#  cd $WORKER_DIR
#  screen -S $WORKER_SCREEN_NAME -d -m $WORKER_COMMAND
#EOF