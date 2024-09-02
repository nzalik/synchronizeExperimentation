#!/bin/bash

G5K_USER_NAME='brickmer'
export DIR="/home/$G5K_USER_NAME" 
export PROM_DIR="$DIR"
export NODES_FILE="$DIR/aware-deployment-grid5k/KubePrep/kube_cluster_prep/nodesfile"
export PROM_NODE=$(tail -1 $NODES_FILE |  cut -d "." -f 1)
#export PROM_NODE=$(sed '1!d' $NODES_FILE)
export PROM_NODE_NAME="$PROM_NODE.lille.grid5000.fr"
export FRONTEND_NODE=$(sed '5!d' $NODES_FILE)
export MIDDLE_NODE=$(sed '4!d' $NODES_FILE)
export BACKEND_NODE=$(sed '3!d' $NODES_FILE)
export FRONTEND_NODE_NAME="$FRONTEND_NODE.lille.grid5000.fr"
export MIDDLE_NODE_NAME="$MIDDLE_NODE.lille.grid5000.fr"
export BACKEND_NODE_NAME="$BACKEND_NODE.lille.grid5000.fr"

