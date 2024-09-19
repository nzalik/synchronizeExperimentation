# shellcheck disable=SC1113
#/!/bin/bash

helm install socialnetwork ../benchmarks/DeathStarBench/socialNetwork/helm-chart/socialnetwork/
kubectl rollout status deployment nginx-thrift
#kubectl get svc jaeger -n default -o yaml > jaeger-latest.yaml
#kubectl apply -f jaeger-internal.yaml
#kubectl apply -f jaeger-external.yaml
#kubectl patch svc jaeger -n default --type='json' -p='[{"op":"replace","path":"/spec/type","value":"NodePort"},{"op":"add","path":"/spec/ports/0/nodePort","value":30575},{"op":"add","path":"/spec/ports/1/nodePort","value":30631},{"op":"add","path":"/spec/ports/2/nodePort","value":30632},{"op":"add","path":"/spec/ports/3/nodePort","value":30578},{"op":"add","path":"/spec/ports/4/nodePort","value":31686},{"op":"add","path":"/spec/ports/5/nodePort","value":31268},{"op":"add","path":"/spec/ports/6/nodePort","value":31411}]'
kubectl apply -f nginx-thrift-nodeport.yaml
kubectl apply -f media-frontend-nodeport.yaml
#kubectl apply -f jaeger-nodeport.yaml

host_name=$(kubectl get pod --selector 'app=nginx-thrift' -o jsonpath='{.items[*].spec.nodeName}')
host_ip=$(kubectl get node $host_name -o jsonpath='{.status.addresses[0].address}')

echo "Social network accessible at $host_ip:30080"
#echo "Jaeger accessible at $host_ip:31686"
