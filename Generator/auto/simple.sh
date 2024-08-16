#!/bin/bash

NODE_SSH_HOST=$1

# shellcheck disable=SC2034
DEPLOY_SCREEN_NAME="deployment1"

echo "Script deployment with : $1"

# shellcheck disable=SC2087
ssh "$NODE_SSH_HOST" << EOF

  pwd
  echo "le path dedepart"
  echo "$PATH"

  kubectl

  export PATH="$HOME/.local/bin:$PATH"

 echo $KUBECONFIG

 export KUBECONFIG=/home/ykoagnenzali/admin.conf

  echo "après"

  echo "$PATH"

  kubectl
EOF