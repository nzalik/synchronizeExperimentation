#!/bin/bash

# Définir le KUBECONFIG
export KUBECONFIG=/home/erods-chouette/admin_k8s_chouette.conf

# Télécharger et extraire Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.23.1

# Ajouter Istio au PATH
export PATH=$PWD/bin:$PATH

# Installer Istio
istioctl install --set profile=demo -y

# Activer l'injection automatique d'Istio sur le namespace par défaut
kubectl label namespace default istio-injection=enabled

# Déployer l'exemple d'application Bookinfo
kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml

# Vérifier le déploiement
kubectl get services
kubectl get pods
kubectl exec "$(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}')" -c ratings -- curl -sS productpage:9080/productpage | grep -o "<title>.*</title>"

# Configurer le gateway Istio
kubectl apply -f samples/bookinfo/networking/bookinfo-gateway.yaml
istioctl analyze

# Récupérer les informations du gateway Istio
kubectl get svc istio-ingressgateway -n istio-system
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
export SECURE_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].nodePort}')
export INGRESS_HOST=$(kubectl get po -l istio=ingressgateway -n istio-system -o jsonpath='{.items[0].status.hostIP}')
export GATEWAY_URL="http://$INGRESS_HOST:$INGRESS_PORT"
export PRODUCTPAGE_URL="$GATEWAY_URL/productpage"

echo $PRODUCTPAGE_URL

# Déployer les addons Istio
kubectl apply -f samples/addons/
kubectl get pods

# Surveiller le déploiement de Kiali
kubectl rollout status deployment/kiali -n istio-system
istioctl dashboard kiali

# Tester l'application Bookinfo
echo $GATEWAY_URL
kubectl get pods
for i in $(seq 1 100); do curl -s -o /dev/null "$GATEWAY_URL/productpage"; done
istioctl dashboard kiali