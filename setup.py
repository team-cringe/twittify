#!/usr/bin/env python

import logging
import argparse

import os
import grp
import getpass
import subprocess
import re

configs = [config
           for config in os.listdir('../istio')
           if os.path.isfile(config)]


def run(command) -> (str, str, int):
    result = subprocess.run(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    error = result.stderr.decode('utf-8')
    code = result.returncode

    return output, error, code


def is_root() -> bool:
    return os.getuid() != 0


def in_group(group) -> bool:
    user = getpass.getuser()
    groups = [g.gr_name
              for g in grp.getgrall()
              if user in g.gr_mem]

    return group in groups


def clean_up():
    logging.info('Removing Kubernetes units')
    for config in configs:
        run(['kubectl', 'delete', '-f', config])


def check_istio(cloud):
    logging.info('Checking Istio installation')
    status, _, _ = run(['kubectl', 'get', 'namespaces'])
    if not bool(re.search(r'istio-system', status)):
        logging.info('Istio is not installed on cluster')
        logging.info('Installing Istio')
        _, error, _ = run(['command', '-v', 'istioctl'])
        run(['istioctl', 'install', '--set', 'profile=demo', '-y'])


def add_istio_label():
    status, _, code = run(['kubectl', 'get', 'namespace', 'default', '--show-labels'])
    if not bool(re.search(r'istio-injection=enabled', status)):
        run(['kubectl', 'label', 'namespace', 'default', 'istio-injection=enabled'])


def upload_units():
    logging.info('Uploading Kubernetes units')
    for config in configs:
        run(['kubectl', 'apply', '-f', config])


def check_minikube():
    status, _, _ = run(['minikube', 'status'])
    logging.info('Checked status of Minikube')
    if not bool(re.search(r'(host|kubelet|apiserver|kubeconfig): Running', status)):
        logging.warning('Minikube is not started. Launching...')
        status, error, _ = run(['minikube', 'start'])
        if error != '':
            logging.error('Cannot start Minikube')
            exit(1)


if __name__ == '__main__':
    pass
