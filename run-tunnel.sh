#!/usr/bin/env bash

if [[ $EUID -eq 0 ]]; then
  echo "Script should not be executed with root privileges"
  exit 1
fi


INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
export INGRESS_PORT
SECURE_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].nodePort}')
export SECURE_INGRESS_PORT
INGRESS_HOST=$(minikube ip)
export INGRESS_HOST

GATEWAY_URL=http://$INGRESS_HOST:$INGRESS_PORT

echo "when minikube tunnel starts, Twittify will be listen on $GATEWAY_URL"

minikube tunnel
