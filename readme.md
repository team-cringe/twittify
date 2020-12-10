## How to launch app on Minikube cluster

We assume you have the following dependencies: 
- docker
- minikube
- kubectl
- istioctl

Your user must be in docker group.

To launch cluster, you should run istio-setup.sh.

To access client, run run-tunnel.sh. It will output:
```
When minikube tunnel starts, Twittify will listen on http://192.168.49.2:PORT
```
Where http://192.168.49.2:PORT is address of our cluster. Client is located at http://192.168.49.2:PORT/client.