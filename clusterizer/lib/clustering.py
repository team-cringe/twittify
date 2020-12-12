from .parsing import *

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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Get NLTK data.
nltk.data.path.append(os.path.abspath(os.getcwd() + '/data'))
nltk.download('stopwords', download_dir='./data/')

# Fill in stopwords.
stopwords = set(nltk.corpus.stopwords.words('russian'))
stopwords.update(nltk.corpus.stopwords.words('english'))
stopwords.update(
    ['че', 'чё', 'ммм', 'аля', 'ой', 'тип', 'блять', 'блядь',
     'хуй', 'пизда', 'тм', 'via', 'lt', 'gt', 'нахуй', 'бля',
     'хд', 'хз', 'ебать', 'пиздец', 'щас', 'свой', 'своя', 'свои',
     'мой', 'моя', 'мои', 'самый', 'вообще', 'блин', 'ах', 'ахах',
     'ла', 'ля', 'чо', 'што', 'lol', 'як', 'шо', 'це'])
stopwords.update(stop_words.get_stop_words('russian'))

# Initialize the morphological analyser.
stem = pymystem3.Mystem()


def process_tweets(tweets) -> str:
    """
    Analyze text of tweets and keep only meaningful words.

    Parameters:
        tweets: List of strings representing tweets.

    Return:
        String with words separated by space.
    """
    result = []
    for t in tweets:
        text = []
        # Remove URLs.
        tweet = remove_word_if(t, is_url)
        # Remove mentions.
        tweet = remove_word_if(tweet, is_mention)
        # Remove words with postfixes.
        # They interfere with TF-IDF procedure.
        tweet = remove_word_if(tweet, has_postfix)
        tweet = tweet.lower()

        for w in stem.lemmatize(tweet):
            word = w.strip()
            if not word == '' \
                    and not is_number(word) \
                    and not is_emoji(word) \
                    and not is_symbol(word) \
                    and word not in stopwords:
                try:
                    analysis = stem.analyze(word)[0]['analysis']
                    # If a word cannot be analysed, save it.
                    # It may be a unique tag.
                    if not analysis:
                        text.append(word)
                    else:
                        group = analysis[0]['gr'].split(',')[0]
                        # Save only nouns and verbs.
                        if group in ['V', 'S']:
                            text.append(word)
                except (IndexError, KeyError):
                    continue
        result.append(' '.join(text))

    return ' '.join(result)


class Clusterizer:
    """
    This class is responsible for obtaining and clustering data from an Elasticsearch instance.
    """

    def __init__(self, elastic):
        """
        Establish connection to Elasticsearch.

        Parameters:
            elastic (str): URI of an Elasticsearch instance.
        """

        self.processed = False
        self.df = DataFrame.from_es(url=f'http://{elastic}', index='twittify-tweets', compat=7)

        logger.info(f'Established connection to: {elastic}')

    def process(self, n_tweets=10_000):
        """
        Load data from Elasticsearch instance to Pandas dataframe and process it.

        Parameters:
            n_tweets (int): Maximum number of tweets to extract at once.
        """
        self.df = self.df.filter(self.df.language == 'ru') \
            .limit(n_tweets) \
            .select('nlikes', 'nreplies', 'nretweets', 'tweet', 'username', 'name') \
            .to_pandas()

        logger.info('Loaded DataFrame')

        self.df = self.df.drop(['_index', '_type', '_id', '_score', '_ignored'], axis=1)

        self.df = self.df.groupby(self.df.username).aggregate(list)

        self.df.nlikes = self.df.nlikes.apply(np.mean)
        self.df.nreplies = self.df.nreplies.apply(np.mean)
        self.df.nretweets = self.df.nretweets.apply(np.mean)
        self.df.name = self.df.name.apply(lambda s: s[0])

        logger.info('Started text processing')

        # The most complex procedure.
        self.df.tweet = self.df.tweet.apply(process_tweets)

        logger.info('Processed text')

    def cluster(self, n_clusters=24):
        """
        Consistently apply TF-IDF and KMeans to data.

        Parameters:
            n_clusters (int): Number of clusters to form.
        """
        logger.info('Started clustering')

        tfidf = TfidfVectorizer(min_df=5, max_df=0.95)
        text = tfidf.fit_transform(self.df.tweet)

        try:
            clusters = KMeans(n_clusters=n_clusters).fit(text)
            self.df['cluster'] = clusters.labels_
        except ValueError as e:
            logger.error(e)
            raise ValueError(e)

        logger.info('Finished clustering')

        self.processed = True

    def tags(self, n_tags=10) -> [dict]:
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
        result = [{
            'tags': [tfidf.get_feature_names()[t] for t in np.argsort(r)[-n_tags:]],
            'n': c
        } for c, r in df.iterrows()]

        return result

    def recommend(self, cluster, n=3) -> [dict]:
        """
        Get recommendation of users to subscribe based on a selected cluster.

        Parameters:
            cluster (int): Number of cluster in `df`.
            n (int): Number of users to extract.

        Return:
            List of dictionaries with user info.
        """
        try:
            sample = self.df[self.df.cluster == cluster].sample(n=n)
        except ValueError as e:
            logger.warning(e)
            sample = self.df[self.df.cluster == cluster].sample(n=1)

        recommendation = [{'username': sample.index[u],
                           'fullname': sample.name.iloc[u],
                           'nlikes': sample.nlikes.iloc[u],
                           'nreplies': sample.nreplies.iloc[u],
                           'nretweets': sample.nretweets.iloc[u]}
                          for u in range(sample.shape[0])]

        return recommendation
