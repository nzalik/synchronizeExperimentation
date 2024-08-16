#!/bin/bash

NODE_SSH_HOST=$1
# shellcheck disable=SC2088
WORKER_DIR="~/Experimentations/synchronizeExperimentation"

# shellcheck disable=SC2087
ssh "$NODE_SSH_HOST" << EOF

  cd $WORKER_DIR

  pwd
  export PATH="$HOME/.local/bin:$PATH"
  export KUBECONFIG=/home/ykoagnenzali/admin.conf

  kubectl get nodes
  kubectl create -f ./custom_deployments/teastore-clusterip-1cpu-5giga.yaml

  echo "on vient de finir"
  echo "###############"
EOF