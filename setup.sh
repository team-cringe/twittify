#!/usr/bin/env bash

if [[ $EUID -ne 0 ]] && ! groups | grep -Pq "(\ |^)docker(\ |$)"; then
  echo "Script must be executed as root or user in \"docker\" group. \
    Aborting..."
  exit 1
fi

STAGES=6

# Shortcuts for the names of images
ESIMG="docker.elastic.co/elasticsearch/elasticsearch:7.10.0"
KBIMG="docker.elastic.co/kibana/kibana:7.10.0"
TORIMG="dperson/torproxy:latest"

if [ -x "$(command -v docker)" ]; then
  # Pull required images
  echo "[1/${STAGES}] Pulling required images"
  docker image inspect ${ESIMG} >/dev/null 2>&1 || docker pull ${ESIMG}
  docker image inspect ${KBIMG} >/dev/null 2>&1 || docker pull ${KBIMG}
  docker image inspect ${TORIMG} >/dev/null 2>&1 || docker pull ${TORIMG}

  # Create network, so containers could communicate
  echo "[2/${STAGES}] Creating docker network"
  docker network inspect twittify-network >/dev/null 2>&1 ||
    docker network create twittify-network

  # Set up Elasticsearch
  echo "[3/$STAGES] Deploying Elasticsearch container"
  docker container inspect twittify-elasticsearch >/dev/null 2>&1 ||
    docker run \
      --detach \
      --name twittify-elasticsearch \
      --net twittify-network \
      --publish 9200:9200 \
      --publish 9300:9300 \
      --env "discovery.type=single-node" \
      ${ESIMG}

  # Set up Kibana
  echo "[4/$STAGES] Deploying Kibana container"
  docker container inspect twittify-kibana >/dev/null 2>&1 ||
    docker run \
      --detach \
      --name twittify-kibana \
      --net twittify-network \
      --publish 5601:5601 \
      ${KBIMG}

  # Set up Tor
  echo "[5/$STAGES] Deploying Tor Proxy container"
  docker container inspect twittify-torproxy >/dev/null 2>&1 ||
    sudo docker run \
      --detach \
      --name twittify-torproxy \
      --publish 8118:8118 \
      --publish 9050:9050 \
      ${TORIMG}

  # Start all containers
  echo "[6/$STAGES] Starting containers"
  docker container start twittify-elasticsearch
  docker container start twittify-kibana
  docker container start twittify-torproxy
else
  echo "Docker not found. \
   Consider installing. \
   Aborting..."
  exit 1
fi
