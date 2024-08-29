#!/bin/bash

# Exécute le premier script
echo "Lancement"
echo "|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"

./gnb_no_scaling_upgrade.sh

./gnb_HPA_scaling_upgrade.sh

echo "|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
echo "Operation terminée"
