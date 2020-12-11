## How to set up Twittify on Kubernetes

These steps require you to have a cluster running a compatible version of Kubernetes (1.16, 1.17, 1.18, 1.19). You can use any supported platform, for example Minikube.

### Prerequirements

- [Download and install Istio](https://istio.io/latest/docs/setup/getting-started/#download)

### Setup

To set up Twittify on a cluster, run
```
./setup.py --istio cloud
```
It verifies Istio installation and applies Twittify configs located at /istio to the cluster.

Command
```
./setup.py --istio local
```
also starts Minikube cluster. It can be run only by user in docker group.


### Discovering address of Twittify

To discover address of the cluster, run
```
./setup.py --address
```
It shows address of the Twittify client.

If cluster is running on Minikube, run
```
./setup.py --tunnel
```
It shows address and starts Minikube tunnel.

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