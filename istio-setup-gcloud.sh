#!/usr/bin/env bash

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