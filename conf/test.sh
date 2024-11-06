#!/bin/bash

# Vérifier que le fichier de configuration est passé en argument
if [ -z "$1" ]; then
    echo "Usage: $0 config_file.conf"
    exit 1
fi

# Charger le fichier de configuration
config_file="$1"
source "$config_file"

# Utiliser les variables chargées
echo "Paramètre 1: $BENCHMARK"
echo "Paramètre 2: $WEBUI"
echo "Paramètre 3: $PROMETHEUS_URL"

# Exécuter des commandes avec les paramètres
echo "Running experiment with param1=$param1, param2=$param2, and param3=$param3"
