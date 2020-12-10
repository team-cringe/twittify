import json
import logging
import bottle
import argparse

from bottle import get, post

from clustering import Clusterizer

logging.basicConfig(level=logging.INFO)


@get('/api/tags')
def tags():
    bottle.response.set_header('Content-Type', 'application/json')
    bottle.response.set_header('Cache-Control', 'no-cache')

    logging.info('Received GET')

    return json.dumps({
        'clusters': clusterizer.get_tags()
    })


@post('/api/recommend')
def recommend():
    logging.info('Received POST')

    try:
        data = bottle.request.json()
    except ValueError:
        logging.error('Cannot parse input data of `recommend`')
        return

    if data is None:
        logging.error('Data of `recommend` is empty')
        return

    bottle.response.set_header('Content-Type', 'application/json')
    bottle.response.set_header('Cache-Control', 'no-cache')

    return json.dumps({
        'users': [clusterizer.get_recommendations(tag['n'])
                  for tag in data['tags']]})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cluster Twitter users')
    parser.add_argument('es', help='Address of an Elasticsearch instance')
    parser.add_argument('server', help='IP and port of a scraper server')
    parser.add_argument('--tweets', help='Number of tweets to extract', type=int, default=100_000)
    parser.add_argument('--clusters', help='Number of clusters to form', type=int, default=24)

    arguments = parser.parse_args()

    host = arguments.server.split(':')[0]
    port = arguments.server.split(':')[1]

    clusterizer = Clusterizer(es='http://' + arguments.es)
    clusterizer.process_data(n_tweets=arguments.tweets)
    clusterizer.cluster_data(n_clusters=arguments.clusters)

    logging.info('Processed data. Ready to start a scraper...')

    bottle.run(host=host, port=port)
