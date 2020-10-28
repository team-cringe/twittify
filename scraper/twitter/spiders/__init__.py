import scrapy
import requests
import logging
import json
import re

from requests.exceptions import RequestException
from json import JSONDecodeError

(GUEST_TOKEN_URL, BEARER_TOKEN_URL) = (
    'https://api.twitter.com/1.1/guest/activate.json',
    'https://abs.twimg.com/responsive-web/client-web/main.a8574df5.js'
)

"""
Resulting structure:

{
  "screen_name": ...,
  "profile_image_url_https": ...,
  "description": ...,
  "location": ...,
  "created_at": ...,
  "favourites_count": ...,
  "followers_count": ...,
  "friends_count": ...,
  "statuses_count": ...,
  "listed_count": ...,
  "verified": ...,
  "protected": ...,
  "tweets": [
    "...": {
      "created_at": ...,
      "quote_count": ...,
      "reply_count": ...,
      "retweet_count": ...,
      "favorite_count": ...,
      "lang": ...,
      "full_text": ...,
      "has_media": ...,
      "has_urls": ...,
      "has_mentions": ...,
      "is_quote": ...,
      "is_retweet": ...,
      "mentions": [...]
    },
  ]
}
"""


def build_user_info_url(handle) -> str:
    """
    Build URL to retrieve information of a user.

    :param handle: Twitter @handle of a user.

    :return: URL string.
    """
    return ('https://api.twitter.com/graphql/'
            '4S2ihIKfF3xhp-ENxvUAfQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22'
            f'{handle}%22%2C%22withHighlightedLabel%22%3Atrue%7D')


def build_twitter_url(rest_id, count) -> str:
    """
    Build URL to retrieve full Twitter timeline of a user.

    :param rest_id: REST ID of a user in Twitter API.
    :param count: Number of tweets to retrieve.

    :return: URL string.
    """
    return ('https://api.twitter.com/2/timeline/profile/'
            f'{rest_id}.json'
            '?include_profile_interstitial_type=1'
            '&include_blocking=1'
            '&include_blocked_by=1'
            '&include_followed_by=1'
            '&include_want_retweets=1'
            '&include_mute_edge=1'
            '&include_can_dm=1'
            '&include_can_media_tag=1'
            '&skip_status=1'
            '&cards_platform=Web-12'
            '&include_cards=1'
            '&include_ext_alt_text=true'
            '&include_quote_count=true'
            '&include_reply_count=1'
            '&tweet_mode=extended'
            '&include_entities=true'
            '&include_user_entities=true'
            '&include_ext_media_color=true'
            '&include_ext_media_availability=true'
            '&send_error_codes=true'
            '&simple_quoted_tweet=true'
            '&include_tweet_replies=false'
            f'&userId={rest_id}'
            f'&count={count}'
            '&ext=mediaStats%2ChighlightedLabel')


class TwitterSpider(scrapy.Spider):
    name = 'twitter'

    cache = {}
    # Headers are used in Scrapy requests
    headers = {}

    def __init__(self):
        # Initialize logging library
        logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S',
                            level=logging.INFO)
        logging.info('Scraper was initialized')
        logging.info('Obtaining Bearer Token...')

        # Obtain Bearer Token
        try:
            response = requests.get(BEARER_TOKEN_URL, timeout=10).text
        except RequestException as e:
            logging.error(f'Failed to obtain Bearer Token: {e}')
            return

        tokens = re.findall(r'a="[A-Za-z0-9%]{104}"', response)

        if len(tokens) != 1:
            logging.error(f'Expected one token match, got: {len(tokens)}')
            return

        bearer_token = f'Bearer {tokens[0][3:-1]}'
        logging.info(f'Got Bearer Token: {bearer_token}')

        logging.info('Obtaining Guest Token...')

        # Then obtain Guest Token
        try:
            headers = {'Authorization': bearer_token}
            response = requests.post(GUEST_TOKEN_URL,
                                     headers=headers,
                                     timeout=10).json()
        except (RequestException, JSONDecodeError) as e:
            logging.error(f'Failed to obtain Guest Token: {e}')
            return

        guest_token = response['guest_token']
        logging.info(f'Got Guest Token: {guest_token}')

        # If tokens are obtained, construct header
        self.headers = {
            'Authorization': bearer_token,
            'x-guest-token': guest_token,
        }

    def start_requests(self):
        """
        The first function in pipeline.
        Read users info from `requests.json` and request information on each.
        Then try parsing it in `parse_user`.

        :return: Yielded request with user handle.
        """

        with open('requests.json', 'r') as file:
            users = json.load(file)['users']

        urls = [build_user_info_url(user) for user in users]
        for (user_handle, url) in zip(users, urls):
            logging.info(f'Requesting information for the user {url}')
            yield scrapy.Request(url=url,
                                 callback=self.parse_user,
                                 headers=self.headers,
                                 cb_kwargs={'user_handle': user_handle})

    def parse_user(self, response, user_handle):
        """
        Parse user data in response.

        :param response: Response with data of a user with specified handle.
        :param user_handle: Handle of the user.

        :return: Yielded request with user timeline.
        """
        try:
            common_data = json.loads(response.body)['data']['user']
            user_url = build_twitter_url(common_data['rest_id'], 100)
            data = common_data['legacy']
        except (JSONDecodeError, KeyError) as e:
            logging.error(f'Failed parsing a response: {e}')
            return

        # Select only given features from the response
        # TODO: Convert to time since the epoch?
        features = [
            'screen_name', 'profile_image_url_https', 'description',
            'location', 'created_at', 'favourites_count',
            'followers_count', 'friends_count', 'statuses_count',
            'listed_count', 'verified', 'protected'
        ]
        user_data = {
            feature: data[feature] for feature in features
        }

        logging.info('Successfully parsed user data')
        logging.info(f'Requesting Twitter timeline for the user @{user_handle}')

        yield scrapy.Request(url=user_url,
                             callback=self.parse_timeline,
                             headers=self.headers,
                             cb_kwargs={
                                 'user_handle': user_handle,
                                 'user_data': user_data
                             })

    def parse_timeline(self, response, user_handle, user_data):
        """
        Parse timeline and add useful features to the user dictionary.

        :param response: Response with list of tweets of a user.
        :param user_handle: Handle of the user.
        :param user_data: Data of the user, obtained on previous steps.

        :return: Complete information of the user is written in JSON file.
        """
        try:
            data = json.loads(response.body)['globalObjects']['tweets']
        except (JSONDecodeError, KeyError) as e:
            logging.error(f'Failed to parse a timeline: {e}')
            return

        features = [
            'created_at', 'quote_count',
            'reply_count', 'retweet_count', 'favorite_count',
            'lang', 'full_text'
        ]
        tweets = {}
        for i in data:
            tweets[i] = {
                feature: data[i][feature] for feature in features
            }

            # Check if tweet contains URLs, media or mentions
            entities = data[i]['entities'].keys()
            # Gather mentions
            mentions = [mention['screen_name'] for mention in data[i]['entities']['user_mentions']] \
                if 'user_mentions' in entities \
                else []
            # If tweet is the quote, get handle of the author and put it to mentions
            quote = re.search(r'https://twitter.com/(.+?)/[A-Za-z0-9]*',
                              data[i]['quoted_status_permalink']['expanded']).group(1) \
                if 'quoted_status_id_str' in data[i] else ''
            mentions.append(quote) if not mentions else [quote]

            # TODO: Add tweet frequency, retweet ratio, text to links ratio, etc.
            tweets[i].update({
                'has_media': 'media' in entities,
                'has_urls': 'urls' in entities,
                'has_mentions': 'user_mentions' in entities,
                'is_quote': 'quoted_status_id_str' in data[i],
                'is_retweet': 'retweeted_status_id_str' in data[i],
                'mentions': mentions
            })

        # Finally, merge gathered data
        user_data['tweets'] = tweets

        logging.info(f'Scraped data of the user @{user_handle}')

        with open(f'../data/{user_handle}.json', 'w') as file:
            file.write(json.dumps(user_data))
