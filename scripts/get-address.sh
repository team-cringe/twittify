#!/usr/bin/env bash

INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')

GATEWAY_URL=$INGRESS_HOST:$INGRESS_PORT

echo "You can find twittify client on $GATEWAY_URL/client"