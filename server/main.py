import json
import logging
import bottle

from bottle import get, post

from src.clusterizer import Clusterizer

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
    clusterizer = Clusterizer(es='http://localhost:9200')
    clusterizer.process_data(n_tweets=10_000)
    clusterizer.cluster_data(n_clusters=10)

    logging.info('Processed data. Ready to start a server...')

    bottle.run(host='0.0.0.0', port=7878)
