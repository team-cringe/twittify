import twint


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

    def scrape(self, limit=20):
        """
        Parameters:
            limit (int): Maximum number of following users to extract.
                Default: 20.
        """
        queue = self.usernames.copy()
        while len(self.usernames) < self.limit or self.limit is None:
            try:
                username = queue.pop()
            except KeyError:
                break

            # Tune parameters of Twint query and send request.
            self.config.Username = username
            self.config.Limit = limit / 20
            twint.run.Following(self.config)

            # Get followings of a user.
            following = twint.output.follows_list
            self.usernames.update(following)
            queue.update(following)

        for username in self.usernames:
            self.config.Username = username
            self.config.Limit = None
            self.config.Elasticsearch = self.es
            print(username)
            twint.run.Lookup(self.config)
