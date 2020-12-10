#!/usr/bin/env bash

kubectl rollout restart deployment/twittify-client
kubectl rollout restart deployment/twittify-scraper
kubectl rollout restart deployment/twittify-clusterizer
