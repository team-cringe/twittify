import twint
import logging
import argparse
import requests

logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self, seed, limit=100, proxy='localhost:9050', es='localhost:9200'):
        """
        Parameters:
            seed (str): The initial username from which the class obtain other usernames.
            limit (int): Maximum number of usernames to scrape.
                None: Scrape endlessly.
                Default: 100.
            proxy (str): Colon-separated host and port of a proxy.
                None: Use no proxy.
            es (str): Colon-separated host and port of an Elasticsearch instance.
        """
        logger.setLevel(logging.INFO)

        self.seed = seed
        self.es = es
        self.limit = limit
        self.usernames = {seed}

        # Configure parameters of Twint queries.
        self.config = twint.Config()
        self.config.Store_object = True
        self.config.Hide_output = True
        if proxy is not None:
            self.config.Proxy_host = proxy.split(':')[0]
            self.config.Proxy_port = proxy.split(':')[1]
            self.config.Proxy_type = 'socks5'

            logger.info(f'Set proxy `{proxy}`')

    def scrape(self, following=20, tweets=1000):
        """
        Parameters:
            following (int): Maximum number of following users to extract.
                Default: 20.
            tweets (int): Maximum number of user tweets to extract.
                Default: 1000.
        """
        scraped = 1
        ready = False

        self.config.Elasticsearch = self.es
        self.config.Index_users = 'twittify-users'
        self.config.Index_tweets = 'twittify-tweets'

        while True:
            try:
                username = self.usernames.pop()
            except KeyError:
                self.usernames = {self.seed}
                username = self.seed

            # Tune parameters of a Twint query and send a request.
            self.config.Username = username
            self.config.Limit = following / 20

            if scraped + 1 > self.limit and not ready:
                try:
                    request = requests.post('http://twittify-clusterizer:8787/api/ready',
                                            data={'n': scraped})
                    request.close()
                    ready = True
                except Exception as e:
                    logger.error(e)

                logger.info('Scraped enough')
                logger.info('Sent POST request to clusterizer')

            # Get followings of a user.
            if len(self.usernames) < self.limit:
                try:
                    twint.run.Following(self.config)
                except Exception as e:
                    logger.error(e)
                    continue
                self.usernames.update(twint.output.follows_list)

                logger.info(f'Scraped followings of the user `{username}`')

            logger.info(f'Scraped {scraped} user(s)')
            logger.info(f'In queue: {len(self.usernames)} users')

            # Scrape tweets of a user.
            self.config.Limit = tweets / 20
            try:
                twint.run.Search(self.config)
            except Exception as e:
                logger.error(e)
                continue
            scraped += 1

            logger.info(f'Stored tweets of `{username}` in {self.es}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape Twitter data')
    parser.add_argument('seed', help='A seed user to start scraping with')
    parser.add_argument('--proxy', help='Address of a Tor proxy', default='localhost:9050')
    parser.add_argument('--es', help='Address of an Elasticsearch instance',
                        default='localhost:9200')
    parser.add_argument('--limit', help='Maximum number of users to store in queue', default=1_000)

    arguments = parser.parse_args()

    scraper = Scraper(seed=arguments.seed,
                      limit=arguments.limit,
                      proxy=None,
                      es=arguments.es)
    scraper.scrape(following=50)
