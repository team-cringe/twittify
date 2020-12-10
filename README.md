## How to launch Twittify on a Minikube cluster

### Requirements

- docker
- minikube
- kubectl
- istioctl

User must be in `docker` group.

### Instructions

1. To launch a cluster, run `istio-setup.py`.
2. To access a client, run `run-tunnel.sh`. 
Possible output:
```
When minikube tunnel starts, Twittify will listen on http://192.168.49.2:PORT
```
where

- Address of the cluster: `http://192.168.49.2:PORT`.
- Address of the client: `http://192.168.49.2:PORT/client`.

## How to test Scraper and Clusterizer locally

### Requirements

- pipenv
- docker

### Instructions

1. Start `local-setup.py`.
2. Install dependencies using `pipenv install`.
3. Launch `main.py` in corresponding folders.

Additionally, `local-setup.py` deploys Kibana container.
By default, data is available in a browser at: `localhost:5601`