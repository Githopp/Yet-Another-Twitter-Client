
#from twitter_authenticator import TwitterAuthenticator - comment style because in __init__
import tweepy
#import twitter_credentials - comment style because in __init__
from datetime import datetime

class TwitterAuthenticator:
    """
    Functionality to connect to Twitter API via the tweepy package -

    this class will not be used by the user himself. It is tethered to the TwitterClient class.
    """
    def authenticate_twitter_app(self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
        """
        Description
        -----------
        This functions authenticates with the twitter API via the tweepy package.
        To get access to your own Twitter API credentials, register an account at https://www.twitter.com and visit https://developer.twitter.com/en.html to apply for an API access.

        Parameters
        ----------
        CONSUMER_KEY:           type = str
                                description = Consumer API Key (https://developer.twitter.com/en.html)

        CONSUMER_SECRET:        type = str
                                description = Consumer API Key (https://developer.twitter.com/en.html)

        ACCESS_TOKEN:           type = str
                                description = Access Token (https://developer.twitter.com/en.html)

        ACCESS_TOKEN_SECRET:    type = str
                                description = Access Token (https://developer.twitter.com/en.html)

        Returns
        -------
        <class 'tweepy.auth.OAuthHandler'>

            --> By calling, it instantiates an authentification object
        """
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth

class TwitterClient:
    """
    Functionality for gathering twitter data -

    for now only able to obtain the tweets in a given account timeline as well as user data.
    """
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, twitter_user=None):
        """
        Description
        -----------
        By initializing this class, it automaticly instantiates the TwitterAuthenticator class, generating an access to the twitter API.
        To get access to your own Twitter API credentials, register an account at https://www.twitter.com and visit https://developer.twitter.com/en.html to apply for an API access.

        Parameters
        ----------
        twitter_user:           type = list or None
                                description = The class is instantiated with the Accounts one wants to obtain tweet-data fromself.
                                            If no argument is given, the twitter-user is None and
                                            will set the Account equal to the user given his or her API's credentials
                                default = None

        CONSUMER_KEY:           type = str
                                description = Consumer API Key (https://developer.twitter.com/en.html)

        CONSUMER_SECRET:        type = str
                                description = Consumer API Key (https://developer.twitter.com/en.html)

        ACCESS_TOKEN:           type = str
                                description = Access Token (https://developer.twitter.com/en.html)

        ACCESS_TOKEN_SECRET:    type = str
                                description = Access Token (https://developer.twitter.com/en.html)

        Returns
        -------
        <class 'twitter_client.TwitterClient'>

            --> By calling, it instantiates a TwitterClient Object

        Example(s)
        ----------
        The following examples instantiates a TwitterClient with the account of Donald Trump.

        1.
            >>>> consumer_key = "Example_xyz1"
            >>>> consumer_secret = "Example_xyz2"
            >>>> access_token = "Example_xyz3"
            >>>> access_token_secret = "Example_xyz4"
            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
        """
        self.auth = TwitterAuthenticator().authenticate_twitter_app(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.twitter_client = tweepy.API(self.auth)
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, start_date, end_date, retweets = False, **kargs):
        """
        Description
        -----------
        This function returns the tweet data, using the tweepy package accesing the twitter API.

        Parameters
        ----------
        start_date:                 type = str
                                    description = A date representation in the following format: "YEAR-MONTH-DAY", representing the start date
                                                  from when one wants to obtain the tweets

        end_date:                   type = str
                                    description = A date representation in the following format: "YEAR-MONTH-DAY", representing the end date
                                                  to when one wants to obtain the tweets

        **kargs:                    Other parameters the tweepy cursor accepts
                                    description = See documentation at: http://docs.tweepy.org/en/v3.5.0/

        Returns
        -------
        <class 'list'>

            --> A list by using the tweepy package obtaining the raw tweets via the twitter API

        Example(s)
        ----------
        The following example obtains Donald Trumps tweets from his timeline:

            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_timeline_tweets(start_date = 2019-06-10", end_date = "2019-06-21")
        """
        tweets = []

        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        if retweets:
            for i in self.twitter_user:
                for tweet in tweepy.Cursor(self.twitter_client.user_timeline, tweet_mode = "extended", id = i, **kargs).items():
                    if tweet.created_at < start:
                        break
                    if tweet.created_at < end:
                        tweets.append(tweet)
        else:
            for i in self.twitter_user:
                for tweet in tweepy.Cursor(self.twitter_client.user_timeline, tweet_mode = "extended", id = i, **kargs).items():
                    if tweet.created_at < start:
                        break
                    if ("RT @" not in tweet.full_text) & (tweet.created_at < end):
                        tweets.append(tweet)

        return tweets


    def get_user_data(self, **kargs):
        """
        Description
        -----------
        This function returns the user data, using the tweepy package accesing the twitter API.

        Parameters
        ----------
        **kargs:                    Other parameters the tweepy cursor accepts
                                    description = See documentation at: http://docs.tweepy.org/en/v3.5.0/

        Returns
        -------
        <class 'list'>

            --> A list by using the tweepy package obtaining the raw user data via the twitter API

        Example(s)
        ----------
        The following example obtains Donald Trumps user data from his timeline:

            >>>> twitter_client = TwitterClient(consumer_key, consumer_secret,access_token, access_token_secret, ["realDonaldTrump"])
            >>>> tweets = twitter_client.get_user_data()
        """
        L = []
        for i in self.twitter_user:
            L.append(self.twitter_client.get_user(i, **kargs))
        return L
