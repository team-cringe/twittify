#!/usr/bin/env bash

echo "[INFO] Checking Istio installation"
if ! kubectl get namespaces | grep -q istio-system; then

  echo "[INFO] Istio is not installed on cluster, installing Istio"
  if ! command -v istioctl >/dev/null; then
    echo "[INFO] Not found istioctl, installing"
    curl -L https://istio.io/downloadIstio | sh -
    PATH=$PWD/$(ls ./istio)/bin:$PATH
    export PATH
  fi
  istioctl install --set profile=demo -y
fi
echo

kubectl get namespace default --show-labels | grep -q istio-injection=enabled ||
  kubectl label namespace default istio-injection=enabled

echo "[INFO] Uploading Kubernetes units"
for config in ./istio/*; do
  kubectl apply -f "$config"
done
echo

echo "[INFO] All done"
