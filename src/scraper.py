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
        queued = 1
        scraped = 0

        self.config.Elasticsearch = self.es
        self.config.Index_users = 'twittify-users'
        self.config.Index_tweets = 'twittify-tweets'

        while len(self.usernames) != 0:
            username = self.usernames.pop()

            # Tune parameters of a Twint query and send a request.
            self.config.Username = username
            self.config.Limit = following / 20

            # Get followings of a user.
            if self.limit is None or queued < self.limit:
                try:
                    twint.run.Following(self.config)
                except Exception:
                    continue
                queued += len(twint.output.follows_list)
                self.usernames.update(twint.output.follows_list)

            logger.info(f'Scraped followings of the user `{username}`')
            logger.info(f'Scraped {scraped} out of {self.limit}')

            # Scrape tweets of a user.
            self.config.Limit = tweets / 20
            try:
                twint.run.Search(self.config)
            except Exception:
                continue
            scraped += 1

            logger.info(f'Stored tweets of `{username}` in {self.es}')
