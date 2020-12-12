import json
import logging
import bottle
import argparse

from bottle import get, post
from lib import Clusterizer


@get('/api/tags')
def tags():
    if not clusterizer.processed:
        return bottle.HTTPResponse(status=403)

    bottle.response.set_header('Content-Type', 'application/json')

    return json.dumps({'clusters': clusterizer.tags()})


@post('/api/ready')
def ready():
    logging.info('Scraper is ready')
    logging.info('Starting analysis')

    clusterizer.process(n_tweets=arguments.tweets)
    clusterizer.cluster(n_clusters=arguments.clusters)

    logging.info('Defined clusters')
    logging.info('Clusterizer is launching')


@post('/api/recommend')
def recommend():
    if not clusterizer.processed:
        return bottle.HTTPResponse(status=403)

    try:
        data = bottle.request.json
    except Exception as e:
        logging.error(e)
        return

    if data is None:
        logging.error('User data is empty')
        return

    bottle.response.set_header('Content-Type', 'application/json')

    return json.dumps({'users': [
        user for tag in data['tags']
        for user in clusterizer.recommend(tag['n'])
    ]})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cluster Twitter users')

    parser.add_argument('--elastic', help='Address of an Elasticsearch instance', default='localhost:9200')
    parser.add_argument('--server', help='IP and port of a Clusterizer server', default='0.0.0.0:8787')
    parser.add_argument('--tweets', help='Number of tweets to extract', type=int, default=2_000_000)
    parser.add_argument('--clusters', help='Number of clusters to form', type=int, default=18)

    arguments = parser.parse_args()

    clusterizer = Clusterizer(elastic=arguments.elastic)

    host = arguments.server.split(':')[0]
    port = arguments.server.split(':')[1]

    bottle.run(host=host, port=port)
