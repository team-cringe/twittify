import twint
import logging
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Scraper:
    def __init__(self, seed, proxy, elastic, cluster):
        """
        Parameters:
            seed (str): The initial username from which the class obtain other usernames.
            proxy (str): Colon-separated host and port of a proxy.
                None: Use no proxy.
            elastic (str): Colon-separated host and port of an Elasticsearch instance.
            cluster (str): Colon-separated host and port of a Clusterizer instance.
        """
        self.elastic = elastic
        self.cluster = cluster
        self.seed = seed
        self.queue = set(seed)

        # Configure parameters of Twint queries.
        self.config = twint.Config()
        self.config.Store_object = True
        self.config.Hide_output = True
        if proxy is not None:
            self.config.Proxy_host = proxy.split(':')[0]
            self.config.Proxy_port = proxy.split(':')[1]
            self.config.Proxy_type = 'socks5'

            logger.info(f'Set proxy: {proxy}')

    def scrape(self, following, tweets, limit):
        """
        Parameters:
            following (int): Maximum number of following users to extract.
                Default: 20.
            tweets (int): Maximum number of user tweets to extract.
                Default: 1000.
            limit (int): Maximum number of usernames to scrape.
                None: Scrape endlessly.
                Default: 100.
        """
        scraped = 0
        batches = 0

        self.config.Elasticsearch = self.elastic
        self.config.Index_users = 'twittify-users'
        self.config.Index_tweets = 'twittify-tweets'

        while True:
            try:
                username = self.queue.pop()
            except KeyError:
                username = set(self.seed)

            # Tune parameters of a Twint query and send a request.
            self.config.Username = username
            self.config.Limit = int(following / 20)

            if scraped > limit:
                self.inform(scraped, batches)
                scraped = 0
                batches += 1

            # Get followings of a user.
            if len(self.queue) < limit:
                try:
                    self.config.Store_object = True
                    twint.run.Following(self.config)
                    self.queue.update(twint.output.follows_list)
                    twint.output.follows_list = []
                except Exception as e:
                    logger.error(e)
                    continue

                logger.info(f'Scraped followings of: {username}')

            logger.info(f'Scraped: {scraped}')
            logger.info(f'Batches: {batches}')
            logger.info(f'In queue: {len(self.queue)}')

            # Scrape tweets of a user.
            self.config.Limit = int(tweets / 20)
            try:
                self.config.Store_object = False
                twint.run.Search(self.config)
                scraped += 1
            except Exception as e:
                logger.error(e)
                continue

            logger.info(f'Stored tweets of: {username}')

    def inform(self, scraped, batches):
        """
        Send POST request to Clusterizer to inform that scraped data is sufficient.

        Parameters:
            scraped (int): Number of scraped users.
            batches (int): Number of already scraped batches.
        """
        address = f'http://{self.cluster}/api/ready'

        try:
            request = requests.post(address, data={'scraped': scraped})
            request.close()
        except Exception as e:
            logger.error(e)

        logger.info(f'Scraped new batch: {batches}')
        logger.info(f'Informed Clusterizer: {self.cluster}')
