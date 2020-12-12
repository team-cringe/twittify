from lib import Scraper

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape Twitter data')

    parser.add_argument('--seed', help='Users to start scraping with', nargs='+', default=['MedvedevRussia'])
    parser.add_argument('--proxy', help='Address of a Tor proxy', default=None)
    parser.add_argument('--elastic', help='Address of an Elasticsearch instance', default='localhost:9200')
    parser.add_argument('--cluster', help='Address of a Clusterizer instance', default='localhost:8787')
    parser.add_argument('--following', '-f', help='Maximum number of followings to extract', type=int, default=50)
    parser.add_argument('--tweets', '-t', help='Maximum number of tweets per user to extract', type=int, default=2000)
    parser.add_argument('--limit', '-l', help='Maximum number of users to store in queue', type=int, default=1000)

    args = parser.parse_args()

    scraper = Scraper(seed=args.seed, proxy=args.proxy, elastic=args.elastic, cluster=args.cluster)
    scraper.scrape(following=args.following, tweets=args.tweets, limit=args.limit)
