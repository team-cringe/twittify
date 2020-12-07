import twint
import logging

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
        queue = self.usernames.copy()
        while len(self.usernames) < self.limit or self.limit is None:
            try:
                username = queue.pop()
            except KeyError:
                logging.warning('Scraped less than limit')
                break

            # Tune parameters of Twint query and send request.
            self.config.Username = username
            self.config.Limit = following / 20
            twint.run.Following(self.config)

            # Get followings of a user.
            following = twint.output.follows_list
            self.usernames.update(following)
            queue.update(following)

            logger.info(f'Scraped following of the user `{username}`')
            logger.info(f'Scraped {len(self.usernames)} out of {self.limit}')

        self.config.Elasticsearch = self.es

        for username in self.usernames:
            self.config.Username = username
            self.config.Limit = tweets / 20
            self.config.Index_users = 'twittify-users'
            self.config.Index_tweets = 'twittify-tweets'

            twint.run.Search(self.config)

            logger.info(f'Set tweets of `{username}` to DB')
