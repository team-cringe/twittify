#!/usr/bin/env bash

if [[ $EUID -eq 0 ]]; then
  echo "Script should not be executed with root privileges"
  exit 1
fi

if ! groups | grep -Pq "(\ |^)docker(\ |$)"; then
  echo "Script must be executed by user in \"docker\" group. \
    Aborting..."
  exit 1
fi

docker info > /dev/null || exit 1

echo "[INFO] Checking Minikube status"
minikube_status=$(minikube status)
if ! ( echo "$minikube_status" | grep -q "^host: Running$" ) ||
  ! ( echo "$minikube_status" | grep -q "^kubelet: Running$" ) || 
  ! ( echo "$minikube_status" | grep -q "^apiserver: Running$" ) || 
  ! ( echo "$minikube_status" | grep -q "^kubeconfig: Configured$" ); then
  echo "[INFO] Minikube is not running, starting Minikube cluster"
  minikube start || exit 1
fi
echo

echo "[INFO] Checking Istio installation"
if ! kubectl get namespaces | grep -q istio-system; then
  echo "[INFO] Istio is not installed on cluster, installing Istio"
  istioctl install --set profile=demo -y
fi
echo

kubectl get namespace default --show-labels | grep -q istio-injection=enabled || \
  kubectl label namespace default istio-injection=enabled

echo "[INFO] Uploading Kubernetes units"
for config in ./istio/*; do
  kubectl apply -f "$config";
done
echo

echo "[INFO] All done"