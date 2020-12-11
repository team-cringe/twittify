#!/usr/bin/env bash

echo "[INFO] Removing Kubernetes units"
for config in ../istio/*; do
  kubectl delete -f "$config"
done
echo
