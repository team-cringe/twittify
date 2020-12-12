#!/usr/bin/env python3

import argparse
import subprocess

global pods
global images

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup Twittify Application')

    parser.add_argument('--istio', '-i', help='Start Istio cluster and upload Kubernetes units',
                        nargs='?', choices=['local', 'cloud'])
    parser.add_argument('--cleanup', '-c', help='Clean up Kubernetes units', action='store_true')
    parser.add_argument('--restart', '-r', help='Restart pods', required=False, nargs='*')
    parser.add_argument('--run', help='Run Minikube tunnel', action='store_true')
    parser.add_argument('--address', '-a', help='Discover address of a cluster', action='store_true')
    parser.add_argument('--test', '-t', help='Test Scraper and Clusterizer locally', action='store_true')
    parser.add_argument('--update', '-u', help='Update Docker images on Docker Hub', nargs='*')

    arguments = parser.parse_args()

    if arguments.istio is not None:
        if arguments.istio == 'local':
            subprocess.run(['./scripts/istio-setup-local.sh'])
        if arguments.istio == 'cloud':
            subprocess.run(['./scripts/istio-setup-gcloud.sh'])
    elif arguments.cleanup:
        subprocess.run(['./scripts/cleanup.sh'])
    elif arguments.restart is not None:
        pods = ['client', 'scraper', 'clusterizer']
        if arguments.restart != [] and arguments.restart != ['all']:
            pods = arguments.restart
        for pod in pods:
            subprocess.run(['kubectl', 'rollout', 'restart', f'deployment/twittify-{pod}'])
    elif arguments.run:
        subprocess.run(['./scripts/run-tunnel.sh'])
    elif arguments.address:
        subprocess.run(['./scripts/get-address.sh'])
    elif arguments.test:
        subprocess.run(['./scripts/local-setup.py'])
    elif arguments.update is not None:
        images = ['clusterizer', 'scraper']
        if arguments.update != [] and arguments.update != ['all']:
            images = arguments.update
        for image in images:
            subprocess.run(['docker', 'build', '-t', f'dikuchan/twittify-{image}', f'./{image}'])
            subprocess.run(['docker', 'push', f'dikuchan/twittify-{image}'])
    else:
        print('Consider checking README.md')
        parser.print_help()
