from src.scraper import Scraper
from src.clusterizer import Clusterizer

if __name__ == '__main__':
    c = Clusterizer()
    c.process_data(n_tweets=1_000)
    c.cluster_data(n_clusters=24)
    tags = c.get_cluster_tags(n_tags=10)

    print(tags)

    # Scraper(seed='MedvedevRussia', limit=10000) \
    #     .scrape(following=10, tweets=200)
