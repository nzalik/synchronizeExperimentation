#!/bin/bash

NODE_SSH_HOST=$1

# shellcheck disable=SC2034
DEPLOY_SCREEN_NAME="deployment1"

echo "Script deployment with : $1"

# shellcheck disable=SC2087
ssh "$NODE_SSH_HOST" << EOF

  export PATH="$HOME/.local/bin:$PATH"
  export KUBECONFIG=/home/ykoagnenzali/admin.conf
  kubectl
  kubectl get nodes
  kubectl get config
  echo "on vient de finir"
  echo "###############"
EOF