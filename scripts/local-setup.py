#!/usr/bin/env python

import subprocess
import sys
import getpass
import grp
import os

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
        print(p.stderr.decode('utf-8'))
        exit(1)


if __name__ == '__main__':
    user = getpass.getuser()
    if os.getuid() != 0 and \
            'docker' not in [group.gr_name
                             for group in grp.getgrall()
                             if user in group.gr_mem]:
        print('Script Script must be executed as root or user in `docker` group. Aborting',
              file=sys.stderr)
        exit(1)

    p = subprocess.run('command -v docker', shell=True, text=True, stdout=subprocess.PIPE)
    if p.returncode != 0:
        print('Docker not found. Aborting...', file=sys.stderr)
        exit(1)

    print('[1/4] Pulling images')
    for image in images.values():
        pull(image)

    print('[2/4] Setting up network')
    network('twittify-network')

    print('[3/4] Deploying containers')
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

    print('[4/4] Starting instances')
    for container in images.keys():
        start(container)
