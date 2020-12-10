import pandas as pd
import numpy as np

from pandasticsearch import DataFrame
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

import os
import nltk
import pymystem3
import stop_words

import logging

from parsing import *

logger = logging.getLogger(__name__)

# Get NLTK data.
nltk.data.path.append(os.path.abspath(os.getcwd() + '/data'))
nltk.download('stopwords', download_dir='./data/')

# Fill in stopwords.
stopwords = set(nltk.corpus.stopwords.words('russian'))
stopwords.update(['че', 'ммм', 'аля', 'ой'])
stopwords.update(stop_words.get_stop_words('russian'))

stem = pymystem3.Mystem()


def process_tweets(tweets):
    result = []
    for t in tweets:
        text = []
        tweet = remove_word_if(t, is_url)
        tweet = remove_word_if(tweet, is_mention)
        tweet = tweet.lower()
        for w in stem.lemmatize(tweet):
            word = w.strip()
            if not word == '' \
                    and not is_number(word) \
                    and not is_emoji(word) \
                    and not is_symbol(word) \
                    and word not in stopwords:
                text.append(word)
        result.append(' '.join(text))
    return ' '.join(result)


class Clusterizer:
    """
    This class is responsible for obtaining and clustering data from Elasticsearch instance.
    """

    def __init__(self, es='http://localhost:9200', index='twittify-tweets'):
        """
        Establish connection to Elasticsearch.

        Parameters:
            es (str): URI of an Elasticsearch instance.
            index (str): Name of data index in the instance.
        """
        logger.setLevel(logging.INFO)

        self.text = None
        self.clusters = None
        self.df = DataFrame.from_es(url=es, index=index, compat=7)

        logger.info(f'Established connection to `{es}`')

    def process_data(self, n_tweets=10_000):
        """
        Load data from Elasticsearch instance to Pandas dataframe and process it.

        Parameters:
            n_tweets (int): Maximum number of tweets to extract at once.
        """
        self.df = self.df.filter(self.df.language == 'ru') \
            .limit(n_tweets) \
            .select('nlikes', 'nreplies', 'nretweets', 'tweet', 'username', 'name') \
            .to_pandas()

        logger.info('Loaded dataset to Pandas dataframe')

        self.df = self.df.drop(['_index', '_type', '_id', '_score', '_ignored'], axis=1)

        self.df = self.df.groupby(self.df.username).aggregate(list)

        self.df.nlikes = self.df.nlikes.apply(np.mean)
        self.df.nreplies = self.df.nreplies.apply(np.mean)
        self.df.nretweets = self.df.nretweets.apply(np.mean)
        self.df.tweet = self.df.tweet.apply(process_tweets)
        self.df.name = self.df.name.apply(lambda s: s[0])

        logger.info('Processed data')

    def cluster_data(self, n_clusters=24):
        """
        Consistently apply TF-IDF and KMeans to data.

        Parameters:
            n_clusters (int): Number of clusters to form.
        """
        logger.info('Start cluster procedure...')

        tfidf = TfidfVectorizer(min_df=5, max_df=0.95)
        self.text = tfidf.fit_transform(self.df.tweet)

        try:
            self.clusters = KMeans(n_clusters=n_clusters).fit(self.text)
            self.df['cluster'] = self.clusters.labels_
        except ValueError as e:
            logger.error(f'{e} Consider changing the number of clusters')

            raise ValueError(e)

        logger.info('Finished cluster procedure')

    def get_tags(self, n_tags=10) -> [dict]:
        """
        Get the most common keywords of each cluster.

        Parameters:
            n_tags (int): Number of words for each cluster to get.

        Return:
            List of dictionaries with mapping of cluster number and tags.
        """
        corpus = self.df.groupby(self.df.cluster) \
            .aggregate(list) \
            .tweet \
            .apply(' '.join)
        tfidf = TfidfVectorizer(min_df=5, max_df=0.95)
        text = tfidf.fit_transform(corpus)

        df = pd.DataFrame(text.todense())
        result = [
            {'tags': [tfidf.get_feature_names()[t]
                      for t in np.argsort(r)[-n_tags:]],
             'n': c}
            for c, r in df.iterrows()
        ]

        return result

    def get_recommendations(self, cluster, n=3) -> [str]:
        """
        Get recommendation of users to subscribe based on a selected cluster.

        Parameters:
            cluster (int): Number of cluster in `df`.
            n (int): Number of users to get.

        Return:
            List of user infos.
        """
        sample = self.df[self.df.cluster == cluster].sample(n=n)
        recommended = [{'username': sample.index[u],
                        'fullname': sample.name.iloc[u],
                        'nlikes': sample.nlikes.iloc[u],
                        'nreplies': sample.nreplies.iloc[u],
                        'nretweets': sample.nretweets.iloc[u]}
                       for u in range(sample.shape[0])]

        return recommended
