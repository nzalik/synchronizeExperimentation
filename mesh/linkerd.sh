curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install-edge | sh

export PATH=$HOME/.linkerd2/bin:$PATH

linkerd version

linkerd check --pre

linkerd install --crds | kubectl apply -f -

linkerd install | kubectl apply -f -

linkerd check

export PATH="$HOME/.local/bin:$PATH"

kubectl apply -f ../custom_deployments/teastore-clusterip-1cpu-5giga.yaml

sleep 240

kubectl get -n default deploy -o yaml | linkerd inject - | kubectl apply -f -

linkerd viz install | kubectl apply -f - # install the on-cluster metrics stack


linkerd check


linkerd viz dashboard &
