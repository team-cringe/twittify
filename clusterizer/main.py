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

    logging.info('Received GET on tags')

    if not clusterizer.processed:
        return bottle.HTTPResponse(status=403,
                                   body=json.dumps({}))

    return json.dumps({
        'clusters': clusterizer.get_tags()
    })


@post('/api/ready')
def ready():
    logging.info('Scraper is ready. Starting analysis')

    if clusterizer.processed:
        logging.info('Data was clustered already')
        return

    clusterizer.process_data(n_tweets=arguments.tweets)
    clusterizer.cluster_data(n_clusters=arguments.clusters)

    logging.info('Processed data. Ready to start a scraper...')


@post('/api/recommend')
def recommend():
    logging.info('Received POST on recommend')

    try:
        data = bottle.request.json
    except ValueError:
        logging.error('Cannot parse input data of `recommend`')
        return

    if data is None:
        logging.error('Data of `recommend` is empty')
        return

    bottle.response.set_header('Content-Type', 'application/json')
    bottle.response.set_header('Cache-Control', 'no-cache')

    if not clusterizer.processed:
        return bottle.HTTPResponse(status=403,
                                   body=json.dumps({}))

    users = []
    for tag in data['tags']:
        users.extend(clusterizer.get_recommendations(tag['n']))

    return json.dumps({'users': users})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cluster Twitter users')
    parser.add_argument('es', help='Address of an Elasticsearch instance')
    parser.add_argument('server', help='IP and port of a scraper server')
    parser.add_argument('--tweets', help='Number of tweets to extract', type=int, default=1_000_000)
    parser.add_argument('--clusters', help='Number of clusters to form', type=int, default=24)

    arguments = parser.parse_args()

    host = arguments.server.split(':')[0]
    port = arguments.server.split(':')[1]

    clusterizer = Clusterizer(es='http://' + arguments.es)

    bottle.run(host=host, port=port)
