## SPbU, Grid and Cloud computing (2020)

## Set up Twittify on Kubernetes

### Requirements

- A compatible cluster (*e.g. Minikube*)
- [Kubernetes](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (*1.16 and latter*)
- [Istio](https://istio.io/latest/docs/setup/getting-started/#download)

### Setup

To set up Twittify on a cluster, run `./setup.py --istio cloud`.
It verifies Istio installation and applies Twittify configs located at `istio` to the cluster.

To start a Minikube cluster, run `./setup.py --istio local`. 
User must be in docker group.

### Discover address of Twittify

To discover address of the cluster, run `./setup.py --address` to show address of the Twittify client.

If cluster is running on Minikube, run `./setup.py --tunnel` to show address and starts Minikube tunnel.

## Example of deployment on GKE

- Start up a cluster.
- Attach to the cluster via terminal.
- In terminal run
```
$ git clone https://github.com/team-cringe/twittify
$ cd twittify
$ ./setup.py --istio cloud
```
- If deployment was successful, services would be listed in `Services & Ingress`.
By default, `scraper` must fetch tweets of at least 2500 users for `clusterizer` to start working.
Considering that, the deployment may take quite a long time (*~4 hours*). 
- In order to find out an address of the `client`, run `./setup.py --address`.
- The service should be available when the `clusterizer` is ready.

Visit `35.228.148.166/client` to see how the service works.

## Test Scraper and Clusterizer locally

### Requirements

- [pipenv](https://pypi.org/project/pipenv/)
- [docker](https://docs.docker.com/engine/install/)

### Setup

- Run `./setup.py --test`.
- For each container, install dependencies using `pipenv install`.
- Launch `main.py` in corresponding folders.

Additionally, `setup.py` deploys Kibana container.
By default, data is available in a browser at `localhost:5601`