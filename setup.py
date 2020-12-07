#!/usr/bin/env python

import subprocess
import sys

from progress.bar import IncrementalBar

images = {'twittify-elasticsearch': 'docker.elastic.co/elasticsearch/elasticsearch:7.10.0',
          'twittify-kibana': 'docker.elastic.co/kibana/kibana:7.10.0',
          'twittify-torproxy': 'dperson/torproxy:latest'}


def pull(image):
    command = f'docker image inspect {image} >/dev/null 2>&1 || docker pull {image}'
    process(command)


def network(name):
    command = f'docker network inspect {name} >/dev/null 2>&1 || docker network create {name}'
    process(command)


def deploy(container, parameters):
    check = f'docker container inspect {container} >/dev/null 2>&1 ||'
    commands = [check, 'docker run']
    for parameter, value in parameters.items():
        if value is None:
            commands.append(f'--{parameter}')
        elif isinstance(value, list):
            for v in value:
                commands.append(f'--{parameter} {v}')
        else:
            commands.append(f'--{parameter} {value}')
    commands.append(f'--name {container}')
    commands.append(images[container])
    command = ' '.join(commands)
    process(command)


def start(container):
    command = f'docker container start {container}'
    process(command)


def process(command):
    p = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0 and p.stderr != b'':
        bar.finish()
        print(p.stderr.decode('utf-8'))
        exit(1)
    bar.next()


if __name__ == '__main__':
    # if os.getuid() != 0:
    #    print('Script must be executed as root. Aborting...', file=sys.stderr)
    #    exit(1)

    p = subprocess.run('command -v docker', shell=True, text=True, stdout=subprocess.PIPE)
    if p.returncode != 0:
        print('Docker not found. Aborting...', file=sys.stderr)
        exit(1)

    bar = IncrementalBar('Deploying', max=10)

    bar.message = 'Pulling images'
    for image in images.values():
        pull(image)

    bar.message = 'Setting up network'
    network('twittify-network')

    bar.message = 'Deploying containers'
    deploy('twittify-elasticsearch', {'detach': None,
                                      'net': 'twittify-network',
                                      'publish': ['9200:9200', '9300:9300'],
                                      'env': 'discovery.type=single-node'})
    deploy('twittify-kibana', {'detach': None,
                               'net': 'twittify-network',
                               'link': 'twittify-elasticsearch:elasticsearch',
                               'publish': '5601:5601'})
    deploy('twittify-torproxy', {'detach': None,
                                 'publish': ['8118:8118', '9050:9050']})

    bar.message = 'Starting instances'
    for container in images.keys():
        start(container)

    bar.finish()
